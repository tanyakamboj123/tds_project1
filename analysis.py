import pandas as pd

# Load the data from users.csv
users_df = pd.read_csv("users.csv")

top_users_five_tokyo = users_df.sort_values(by='followers', ascending=False).head(5)['login'].tolist()
print("Ans 1: Top 5 users with the highest number of followers:", ", ".join(top_users_five_tokyo))

# Sort users by the number of followers in descending order and get the top 5
top_users = users_df.sort_values(by="followers", ascending=False).head(5)

# Extract the 'login' column and join the values into a comma-separated string
top_users_logins = ", ".join(top_users["login"])

print("Top 5 users in Tokyo with the highest number of followers:")
print(top_users_logins)

# 2. 5 earliest registered GitHub users in Tokyo

# Step 1: Check the 'created_at' column type
print("Before conversion, 'created_at' type:", users_df['created_at'].dtype)

# Convert 'created_at' to datetime to ensure proper sorting
users_df['created_at'] = pd.to_datetime(users_df['created_at'], errors='coerce')

# Step 2: Verify the conversion
print("After conversion, 'created_at' type:", users_df['created_at'].dtype)
print("Any NaT values (missing dates) after conversion:", users_df['created_at'].isna().sum())

# Step 3: Sort by 'created_at' in ascending order to find the earliest users
earliest_users = users_df.sort_values(by="created_at", ascending=True).head(5)

# Step 4: Verify the sorting by printing the 'created_at' column of the top 5
print("Top 5 earliest 'created_at' values:")
print(earliest_users[['login', 'created_at']])

# Extract the 'login' column and join the values into a comma-separated string
earliest_users_logins = ", ".join(earliest_users["login"])

print("5 earliest registered GitHub users in Tokyo:")
print(earliest_users_logins)


# 4. Which company do the majority of these developers work at?
users_with_company = users_df[users_df['company'].notnull()].copy()  
users_with_company.loc[:, 'company'] = users_with_company['company'].str.strip().str.lstrip('@').str.upper()
most_common_company = users_with_company['company'].value_counts().idxmax()
print("Majority of these developers work at:", most_common_company)

