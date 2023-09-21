import sqlite3
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

conn = sqlite3.connect('amazon_reviews.sqlite3')
df = pd.read_sql_query("SELECT * FROM reviews", conn)

def preprocess_text(text):
    if text is None:
        return ""
    
    text = text.lower()

    text = text.translate(str.maketrans('', '', string.punctuation))

    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    words = [word for word in words if word.isalpha()]

    cleaned_text = ' '.join(words)

    return cleaned_text

negative_reviews = df[df['overall'].isin([1, 2])]
positive_reviews = df[df['overall'].isin([4, 5])]

negative_reviews['review_text'] = negative_reviews['review_text'].apply(preprocess_text)
positive_reviews['review_text'] = positive_reviews['review_text'].apply(preprocess_text)

negative_text = " ".join(review for review in negative_reviews['review_text'])
negative_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(negative_text)

positive_text = " ".join(review for review in positive_reviews['review_text'])
positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_text)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.title('Negative Reviews Word Cloud')
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.title('Positive Reviews Word Cloud')
plt.axis("off")
plt.show()