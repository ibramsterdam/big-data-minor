import pandas as pd
import sqlite3

# import and clean csv
df = pd.read_csv("../data/amazon_reviews_train.csv")
df = df.rename(columns={'reviewerID': 'reviewer_id', 'amazon-id': 'amazon_id', 'helpful': 'helpful', 
                        'unixReviewTime': 'unix_review_time', 'reviewText': 'review_text', 
                        'overall': 'overall', 'reviewTime': 'review_time', 'summary': 'summary', 
                        'price': 'price', 'categories': 'categories', 'root-genre': 'root_genre', 
                        'title': 'title', 'artist': 'artist', 'label': 'label', 
                        'first-release-year': 'first_release_year', 'songs': 'songs', 
                        'salesRank': 'sales_rank', 'related': 'related'})
df.drop(columns=['review_time'], inplace=True)
df['first_release_year'] = pd.to_numeric(df['first_release_year'], errors='coerce').fillna(9999).astype('int64')

# connect to db
conn = sqlite3.connect('amazon_reviews.sqlite3')
cursor = conn.cursor()

#  Seed categories
categories_lists = df['categories'].apply(lambda x: x.strip("[]").replace("'", "").split(", "))
unique_categories = set()

for category_list in categories_lists:
    unique_categories.update(category_list)

for category_name in unique_categories:
    cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))

conn.commit()

# Cet dict of categories
cursor.execute("SELECT category_id, category_name FROM categories")
categories_data = cursor.fetchall()
category_id_dict = {category_name: category_id for category_id, category_name in categories_data}


# Seed products and product_category
unique_amazon_ids_list = df['amazon_id'].unique().tolist()

for amazon_id in unique_amazon_ids_list:
     # Get the first row with the matching amazon_id
    product_info = df[df['amazon_id'] == amazon_id].iloc[0] 

    title = int(product_info['title'])
    artist = int(product_info['artist'])
    label = product_info['label']
    first_release_year = int(product_info['first_release_year'])
    price = float(product_info['price'])
    sales_rank = int(product_info['sales_rank'])
    songs = product_info['songs']

    category_name = product_info['root_genre']
    root_genre = int(category_id_dict.get(category_name, None))

    cursor.execute("INSERT INTO products (amazon_id, title, artist, label, first_release_year, root_genre, price, sales_rank, songs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (amazon_id, title, artist, label, first_release_year, root_genre, price, sales_rank, songs))
    
    
    categories = product_info['categories']
    category_list = [category.strip("[]").replace("'", "") for category in categories.split(", ")]

    for category_name_in_list in category_list:
        category_id = category_id_dict.get(category_name_in_list, None)
        if category_id is not None:
            cursor.execute("INSERT INTO product_category (product_id, category_id) VALUES (?, ?)",
                            (amazon_id, category_id))

conn.commit()

# Seed reviews

for index, row in df.iterrows():
    reviewer_id = row['reviewer_id']
    amazon_id = row['amazon_id']
    unix_review_time = row['unix_review_time']
    review_text = row['review_text']
    overall = row['overall']
    helpful = row['helpful']
    summary = row['summary']
    related = row['related']

    cursor.execute("INSERT INTO reviews (reviewer_id, amazon_id, unix_review_time, review_text, overall, helpful, summary, related) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (reviewer_id, amazon_id, unix_review_time, review_text, overall, helpful, summary, related))

# Commit the changes and close the database connection
conn.commit()
conn.close()