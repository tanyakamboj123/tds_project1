import requests
import pandas as pd
import re

# Replace with your GitHub access token
access_token = "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"
headers = {
    "Authorization": f"token {access_token}"
}

# Step 1: Fetch User Data
url = "https://api.github.com/search/users?q=location:Tokyo+followers:>200&per_page=100&page={page}"
response = requests.get(url, headers=headers)

user_details = []

if response.status_code == 200:
    users_data = response.json()
    users = users_data['items']

    for user in users:
        username = user['login']
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code == 200:
            user_info = user_response.json()
            
            # Clean up company field
            company = user_info.get('company', '')
            if company:
                company = re.sub(r'^\@', '', company.strip()).upper()

            # Append user details
            user_details.append({
                "login": username,
                "name": user_info.get('name', ''),
                "company": company,
                "location": user_info.get('location', ''),
                "email": user_info.get('email', ''),
                "hireable": user_info.get('hireable', False),
                "bio": user_info.get('bio', ''),
                "public_repos": user_info.get('public_repos', 0),
                "followers": user_info.get('followers', 0),
                "following": user_info.get('following', 0),
                "created_at": user_info.get('created_at', '')
            })

# Save user data to users.csv
user_df = pd.DataFrame(user_details)
user_df.to_csv("users.csv", index=False)

# Step 2: Fetch Repository Data
repository_details = []

for user in user_details:
    username = user['login']
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=500"
    repos_response = requests.get(repos_url, headers=headers)
    
    if repos_response.status_code == 200:
        repos = repos_response.json()
        
        for repo in repos:
            repository_details.append({
                "login": username,
                "full_name": repo.get('full_name', ''),
                "created_at": repo.get('created_at', ''),
                "stargazers_count": repo.get('stargazers_count', 0),
                "watchers_count": repo.get('watchers_count', 0),
                "language": repo.get('language', ''),
                "has_projects": repo.get('has_projects', False),
                "has_wiki": repo.get('has_wiki', False),
                "license_name": repo['license']['key'] if repo.get('license') else None
            })

# Save repository data to repositories.csv
repo_df = pd.DataFrame(repository_details)
repo_df.to_csv("repositories.csv", index=False)