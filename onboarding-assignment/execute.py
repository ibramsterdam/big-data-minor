import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the SQLite database and retrieve the data
conn = sqlite3.connect('amazon_reviews.sqlite3')
query = """
SELECT p.price, r.overall
FROM products p
JOIN reviews r ON p.amazon_id = r.amazon_id;
"""
df = pd.read_sql_query(query, conn)

# Remove price outliers using the Interquartile Range (IQR) method
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
price_lower_bound = Q1 - 1.5 * IQR
price_upper_bound = Q3 + 1.5 * IQR
df = df[(df['price'] >= price_lower_bound) & (df['price'] <= price_upper_bound)]

# Calculate the correlation coefficient
correlation_coefficient = df['price'].corr(df['overall'])
print(f"Correlation Coefficient: {correlation_coefficient:.2f}")

# Create a scatter plot with a regression line
plt.figure(figsize=(10, 6))
sns.regplot(x='price', y='overall', data=df, scatter_kws={'alpha':0.3})
plt.title('Price vs. Review Rating (Outliers Removed)')
plt.xlabel('Price')
plt.ylabel('Review Rating')
plt.grid(True)
plt.show()
