import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)



# 1. Read the data into a dataframe
movies = pd.read_csv("../data/imdb_movies.csv")

# 2/3. Select only rows with USA $ sign and strip it
movies = movies[movies["budget"].str.contains("\$", na=False)]
movies["budget"] = movies["budget"].str.replace('$', "")

# 4. make the type numerical
movies["budget"] = movies["budget"].astype("int")
assert movies["budget"].dtype == "int"

# 5. Create a bar plot for the total budget per year
total_budget_per_year = movies.groupby("year")["budget"].sum()

# Create the bar plot
ax = total_budget_per_year.plot(kind="bar", title="Total Budget per Year")
plt.xlabel("year")
plt.ylabel("budget")


# Set the y-axis ticks and labels
ax.set_yticks([0, 2e9, 4e9, 6e9, 8e9, 10e9])
ax.set_yticklabels(['0', '2B', '4B', '6B', '8B', '10B'])

# plt.show()

# 6. Split 'genre' in different columns
genre_columns = movies['genre'].str.get_dummies(sep=', ')
movies = pd.concat([movies, genre_columns], axis=1)

# 7. add a column numberOfActors
movies['actors'] = movies['actors'].fillna('') # clean rows
movies['numberOfActors'] = movies['actors'].str.split(', ').apply(len)
print(movies[['actors', 'numberOfActors']])
# 8. add a column 
movies["mainActor"] = movies["actors"].str.split(",").str[0].str.strip()
print(movies["mainActor"])