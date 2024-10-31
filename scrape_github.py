import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load the GitHub token from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

BASE_URL = "https://api.github.com"


def fetch_users():
    users = []
    page = 1
    print("Fetching users in Bangalore with over 100 followers...")
    while True:
        url = f"{BASE_URL}/search/users?q=location:Bangalore+followers:>100&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print("Error fetching users:", response.json())
            break
        data = response.json().get("items", [])
        if not data:
            print("No more users found.")
            break
        for user in data:
            user_details = fetch_user_details(user["login"])
            if user_details:
                users.append(user_details)
                print(f"User {user_details['login']} fetched successfully.")
        print(f"Page {page} fetched.")
        page += 1
        time.sleep(1)  # To respect rate limits
    print(f"Total users fetched: {len(users)}")
    return users


def fetch_user_details(username):
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching user {username}:", response.json())
        return None
    user = response.json()
    user_data = {
        "login": user.get("login", ""),
        "name": user.get("name", ""),
        "company": clean_company_name(user.get("company", "")),
        "location": user.get("location", ""),
        "email": user.get("email", ""),
        "hireable": user.get("hireable", ""),
        "bio": user.get("bio", ""),
        "public_repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "created_at": user.get("created_at", ""),
    }
    return user_data


def clean_company_name(company):
    if company:
        return company.strip().lstrip("@").upper()
    return ""


def fetch_repositories(username):
    repos = []
    page = 1
    print(f"Fetching repositories for user {username}...")
    while True:
        url = f"{BASE_URL}/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching repos for {username}:", response.json())
            break
        data = response.json()
        if not data:
            print(f"No more repositories found for {username}.")
            break
        for repo in data:
            repo_data = {
                "login": username,
                "full_name": repo.get("full_name", ""),
                "created_at": repo.get("created_at", ""),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", ""),
                "has_projects": repo.get("has_projects", False),
                "has_wiki": repo.get("has_wiki", False),
                "license_name": (
                    repo.get("license", {}).get("key", "")
                    if repo.get("license")
                    else ""
                ),
            }
            repos.append(repo_data)
        print(f"Page {page} of repositories for {username} fetched.")
        if len(data) < 100:
            break
        page += 1
        time.sleep(1)  # To respect rate limits
    print(f"Total repositories fetched for {username}: {len(repos)}")
    return repos


def main():
    # Step 1: Fetch user data
    print("Starting user data collection...")
    users = fetch_users()
    users_df = pd.DataFrame(users)
    users_df.to_csv("data/users.csv", index=False)
    print("User data saved to data/users.csv")

    # Step 2: Fetch repository data for each user
    all_repos = []
    for user in users:
        repos = fetch_repositories(user["login"])
        all_repos.extend(repos)

    # Convert repositories list to DataFrame and save
    repos_df = pd.DataFrame(all_repos)
    repos_df.to_csv("data/repositories.csv", index=False)
    print("Repository data saved to data/repositories.csv")
    print("Data collection complete.")


if __name__ == "__main__":
    main()