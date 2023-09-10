import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# 3. read the data into a dataframe
results = pd.read_csv("../data/football_results.csv")

# 4. print first rows of the dataframe
print(results.head())

# 5. check the information on the website
## a. number of unique 'home' teams
unique_home_teams = results.drop_duplicates(subset="home")
print(unique_home_teams.shape[0])

## b. number of unique 'away' teams
unique_away_teams = results.drop_duplicates(subset="away")
print(unique_away_teams.shape[0])

# 6. Find the teams that are mentioned in the 'away' column but never in the 'home' column
home_set = set(tuple(row) for row in unique_home_teams.values)
away_set = set(tuple(row) for row in unique_away_teams.values)
print("6. ", len(away_set) -  len(home_set))

# 7/8. Add a column 'home_wins', ‘home_draws’, 'homw_loses'
results["home_wins"] = np.where(results["gh"] > results["ga"], 1, 0)
results["home_draws"] = np.where(results["gh"] == results["ga"], 1, 0)
results["home_loses"] = np.where(results["gh"] < results["ga"], 1, 0)

print(results.head())

# 9. which team won the most home games
print(results.groupby("home")["home_wins"].agg([sum, "count"]).sort_values(by="sum", ascending=False))

# 10. pick the unbeatable team
## Group by "home" and calculate the sum and count
grouped = results.groupby("home")["home_wins"].agg(["sum", "count"]).reset_index()

## Filter for teams with at least 50 home games
filtered_result = grouped.groupby("home").filter(lambda x: x["count"].sum() >= 50)
filtered_result["Perc_home_wins"] = filtered_result["sum"] / filtered_result["count"]

print(filtered_result.sort_values(by="Perc_home_wins", ascending=False))

## Filter for teams with at least 500 home games
filtered_result = grouped.groupby("home").filter(lambda x: x["count"].sum() >= 500)
filtered_result["Perc_home_wins"] = filtered_result["sum"] / filtered_result["count"]

print(filtered_result.sort_values(by="Perc_home_wins", ascending=False))

# 11. Plot
dict_of_lists = {
    "home": results.groupby("home")["home"].unique().explode().tolist(),
    "home_wins": results.groupby("home")["home_wins"].agg(["sum"])["sum"].values,
    "home_draws": results.groupby("home")["home_draws"].agg(["sum"])["sum"].values,
    "home_loses": results.groupby("home")["home_loses"].agg(["sum"])["sum"].values,
    "count": results.groupby("home")["home_loses"].agg(["count"])["count"].values
}

plot = pd.DataFrame(dict_of_lists)


filtered_plot = plot.groupby("home").filter(lambda x: x["count"].sum() >= 500)
filtered_plot["Perc_home_wins"] = filtered_plot["home_wins"] / filtered_plot["count"]
filtered_plot["Perc_home_draws"] = filtered_plot["home_draws"] / filtered_plot["count"]
filtered_plot["Perc_home_loses"] = filtered_plot["home_loses"] / filtered_plot["count"]

display = filtered_plot.drop(["count", "home_wins", "home_draws", "home_loses"], axis=1)
display = display.set_index("home")
display = display.sort_values(by="Perc_home_wins", ascending=False)
display = display.head(10)

display.plot(kind="bar", stacked=True, figsize=(10, 6))
plt.title("Stacked Bar Chart of Home Performance")
plt.xlabel("home")
plt.ylabel("Percentage")
plt.show()



# Chatgpt solution
# # Group and aggregate the data
# agg_results = results.groupby("home").agg(
#     home_wins=("home_wins", "sum"),
#     home_draws=("home_draws", "sum"),
#     home_loses=("home_loses", "sum"),
#     count=("home_loses", "count")
# )

# # Filter for teams with at least 500 home games
# filtered_results = agg_results[agg_results["count"] >= 500]

# # Calculate win percentages
# filtered_results["Perc_home_wins"] = filtered_results["home_wins"] / filtered_results["count"]
# filtered_results["Perc_home_draws"] = filtered_results["home_draws"] / filtered_results["count"]
# filtered_results["Perc_home_loses"] = filtered_results["home_loses"] / filtered_results["count"]

# # Sort and select the top 10
# top_10_results = filtered_results.sort_values(by="Perc_home_wins", ascending=False).head(10)

# # Plot the stacked bar chart
# top_10_results[["Perc_home_wins", "Perc_home_draws", "Perc_home_loses"]].plot(kind="bar", stacked=True, figsize=(10, 6))
# plt.title("Stacked Bar Chart of Home Performance")
# plt.xlabel("home")
# plt.ylabel("Percentage")
# plt.show()





