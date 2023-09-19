import pandas as pd
import sqlite3


# import and clearn csv
df = pd.read_csv("../data/amazon_reviews_train.csv")
df = df.rename(columns={'reviewerID': 'reviewer_id', 'amazon-id': 'amazon_id', 'helpful': 'helpful', 
                        'unixReviewTime': 'unix_review_time', 'reviewText': 'review_text', 
                        'overall': 'overall', 'reviewTime': 'review_time', 'summary': 'summary', 
                        'price': 'price', 'categories': 'categories', 'root-genre': 'root_genre', 
                        'title': 'title', 'artist': 'artist', 'label': 'label', 
                        'first-release-year': 'first_release_year', 'songs': 'songs', 
                        'salesRank': 'sales_rank', 'related': 'related'})
df.drop(columns=['review_time'], inplace=True)


print(df.shape)