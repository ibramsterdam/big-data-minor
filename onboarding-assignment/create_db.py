import sqlite3
import pandas as pd

conn = sqlite3.connect('amazon_reviews.sqlite3')
conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key support

create_review_table = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reviewer_id INTEGER,
    amazon_id INTEGER,
    unix_review_time INTEGER,
    review_text TEXT,
    overall INTEGER,
    helpful TEXT,
    summary TEXT,
    related TEXT,
    FOREIGN KEY (amazon_id) REFERENCES products (amazon_id)
);
"""
create_product_table = """
CREATE TABLE IF NOT EXISTS products (
    amazon_id INTEGER PRIMARY KEY,
    title INTEGER,
    artist INTEGER,
    label TEXT,
    first_release_year REAL,
    root_genre INTEGER,
    price REAL,
    sales_rank INTEGER,
    songs TEXT,
    FOREIGN KEY (root_genre) REFERENCES categories (category_id)
);
"""
create_categories_table = """
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT
);
"""
create_product_category_table = """
CREATE TABLE IF NOT EXISTS product_category (
    product_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products (amazon_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);
"""
# Execute the SQL CREATE TABLE statements
conn.execute(create_review_table)
conn.execute(create_product_table)
conn.execute(create_categories_table)
conn.execute(create_product_category_table)