import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Read the data into a dataframe
df = pd.read_csv("../data/bl_flickr_images_book.csv")

# 2. look at the 5 first rows
print(df.head(5))

# 3. look at the number of columns
print(df.shape[1], "columns")

# 4. keep only ['Identifier', 'Place of Publication', 'Date of Publication','Publisher', 'Title', 'Author', 'Flickr URL']
keep_columns = ['Identifier', 'Place of Publication', 'Date of Publication','Publisher', 'Title', 'Author', 'Flickr URL']
new_df = df.loc[:, keep_columns]
print(new_df.head())


# 5. clean up 
unwanted_characters = ['[', ',', '-', "]"]
def clean_dates(dop):
    if isinstance(dop, str):
        for char in unwanted_characters:
            dop = dop.replace(char, '')
    return dop

df['Date of Publication'] = df['Date of Publication'].apply(clean_dates)
print(df['Date of Publication'].head())