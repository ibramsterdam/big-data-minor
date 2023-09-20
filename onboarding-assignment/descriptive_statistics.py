import sqlite3
import pandas as pd

conn = sqlite3.connect('amazon_reviews.sqlite3')
reviews_df = pd.read_sql_query("SELECT * FROM reviews", conn)
products_df = pd.read_sql_query("SELECT * FROM products", conn)

num_reviews = len(reviews_df)
num_reviewers = reviews_df['reviewer_id'].nunique()  # Count of unique reviewer_id values
num_products = len(products_df)

average_price = products_df['price'].mean()
average_review_rating = reviews_df['overall'].mean()

print("Overview of the Dataset:")
print(f"Number of Reviews: {num_reviews}")
print(f"Number of Unique Reviewers: {num_reviewers}")
print(f"Number of Products: {num_products}")
print(f"Average Price: ${average_price:.2f}")
print(f"Average Review Rating: {average_review_rating:.2f}")