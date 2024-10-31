import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import numpy as np

users_df = pd.read_csv("users.csv")
repos_df = pd.read_csv("repositories.csv")

users_df['created_at'] = pd.to_datetime(users_df['created_at'], errors='coerce')

# Question 1: Top 5 users in Berlin with the highest number of followers
top_followed_users = users_df.nlargest(5, 'followers')['login']
top_followed_users_list = ','.join(top_followed_users)
print("1. Top 5 users by followers:", top_followed_users_list)

# Question 2: 5 earliest registered GitHub users in Berlin
earliest_registered_users = users_df.nsmallest(5, 'created_at')['login']
earliest_registered_users_list = ','.join(earliest_registered_users)
print("2. 5 earliest registered users:", earliest_registered_users_list)

# Question 3: 3 most popular licenses among these users
licenses = repos_df['license_name'].dropna()
top_licenses = licenses.value_counts().nlargest(3).index.tolist()
top_licenses_list = ','.join(top_licenses)
print("3. 3 most popular licenses:", top_licenses_list)

# Question 4: The company the majority of these developers work at
users_df['company'] = users_df['company'].str.strip().str.lstrip('@').str.upper()
top_company = users_df['company'].mode().values[0]
print("4. Company with the majority of developers:", top_company)

# Question 5: Most popular programming language among these users
languages = repos_df['language'].dropna()
top_language = languages.value_counts().idxmax()
print("5. Most popular programming language:", top_language)
users_df['created_at'] = pd.to_datetime(users_df['created_at'], errors='coerce')

# Question 6: Second most popular language among users who joined after 2020
users_after_2020 = users_df[users_df['created_at'] > '2020-01-01']
logins_after_2020 = users_after_2020['login']
repos_after_2020 = repos_df[repos_df['login'].isin(logins_after_2020)]
second_popular_language = repos_after_2020['language'].value_counts().index[1]
print("6. Second most popular language among users who joined after 2020:", second_popular_language)

# Question 7: Language with the highest average number of stars per repository
avg_stars_per_language = repos_df.groupby('language')['stargazers_count'].mean()
top_language_by_stars = avg_stars_per_language.idxmax()
print("7. Language with the highest average stars per repository:", top_language_by_stars)

# Question 8: Top 5 users in terms of leader_strength
users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])
top_leader_strength_users = users_df.nlargest(5, 'leader_strength')['login']
top_leader_strength_users_list = ','.join(top_leader_strength_users)
print("8. Top 5 users by leader_strength:", top_leader_strength_users_list)


# Question 9: Correlation between followers and number of public repositories
followers_repos_corr, _ = pearsonr(users_df['followers'], users_df['public_repos'])
print("9. Correlation between followers and public repositories:", round(followers_repos_corr, 3))

# Question 10: Regression slope of followers on public repositories
X = users_df[['public_repos']].values
y = users_df['followers'].values
reg = LinearRegression().fit(X, y)
followers_repos_slope = reg.coef_[0]
print("10. Regression slope of followers on public repositories:", round(followers_repos_slope, 3))

# Question 11: Correlation between having projects enabled and having wiki enabled
repos_df['has_projects'] = repos_df['has_projects'].astype(int)
repos_df['has_wiki'] = repos_df['has_wiki'].astype(int)
projects_wiki_corr, _ = pearsonr(repos_df['has_projects'], repos_df['has_wiki'])
print("11. Correlation between projects and wiki enabled:", round(projects_wiki_corr, 3))

# Question 12: Difference in average following between hireable and non-hireable users
users_df['hireable'] = users_df['hireable'].fillna(False).astype(bool)
avg_following_hireable = users_df[users_df['hireable'] == True]['following'].mean()
avg_following_non_hireable = users_df[users_df['hireable'] == False]['following'].mean()
following_difference = avg_following_hireable - avg_following_non_hireable
print("12. Difference in average following between hireable and non-hireable users:", round(following_difference, 3))

# Question 13: Impact of bio word count on followers (regression slope)
users_with_bio = users_df.dropna(subset=['bio']).copy()
users_with_bio['bio_word_count'] = users_with_bio['bio'].str.split().apply(len)
X_bio = users_with_bio[['bio_word_count']].values
y_followers = users_with_bio['followers'].values
reg_bio = LinearRegression().fit(X_bio, y_followers)
bio_followers_slope = reg_bio.coef_[0]
print("13. Regression slope of followers on bio word count:", round(bio_followers_slope, 3))

# Question 14: Top 5 users by number of repositories created on weekends
repos_df['created_at'] = pd.to_datetime(repos_df['created_at'], errors='coerce')
weekend_repos = repos_df[repos_df['created_at'].dt.weekday >= 5]
top_weekend_creators = weekend_repos['login'].value_counts().nlargest(5).index.tolist()
top_weekend_creators_list = ','.join(top_weekend_creators)
print("14. Top 5 users by repos created on weekends:", top_weekend_creators_list)

# Question 15: Do hireable users share their email addresses more often?
users_df['hireable'] = users_df['hireable'].fillna(False).astype(bool)
hireable_with_email = users_df[users_df['hireable'] & users_df['email'].notna()].shape[0] / users_df[users_df['hireable']].shape[0]
non_hireable_with_email = users_df[~users_df['hireable'] & users_df['email'].notna()].shape[0] / users_df[~users_df['hireable']].shape[0]
email_share_diff = hireable_with_email - non_hireable_with_email
print("15. Difference in email sharing between hireable and non-hireable users:", round(email_share_diff, 3))

# Question 16: Most common surname
users_with_names = users_df.dropna(subset=['name']).copy()
users_with_names['surname'] = users_with_names['name'].str.strip().str.split().str[-1]
surname_counts = users_with_names['surname'].value_counts()
max_surname_count = surname_counts.max()
most_common_surnames = surname_counts[surname_counts == max_surname_count].index.tolist()
most_common_surnames.sort()  # Sort alphabetically if there's a tie
most_common_surnames_list = ','.join(most_common_surnames)
print("16. Most common surname(s):", most_common_surnames_list)