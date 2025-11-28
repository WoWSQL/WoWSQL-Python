"""
WOWSQL Python SDK - Basic Usage Examples
"""

from wowsql import WowSQLClient

# Initialize client with your project URL and API key
client = WowSQLClient(
    project_url="https://your-project.wowsql.com",
    api_key="your-api-key-here"
)

# 1. SELECT - Get all users
print("=== SELECT ALL USERS ===")
response = client.table("users").select("*").execute()
print(f"Found {response.count} users")
for user in response.data:
    print(f"  - {user['name']} ({user['email']})")

# 2. SELECT with filters
print("\n=== SELECT ACTIVE USERS ===")
active_users = client.table("users") \
    .select("id", "name", "email") \
    .eq("status", "active") \
    .limit(5) \
    .execute()
print(f"Active users: {active_users.count}")

# 3. INSERT - Add new user
print("\n=== INSERT NEW USER ===")
new_user = client.table("users").insert({
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "status": "active"
}).execute()
print(f"Inserted user: {new_user.data}")

# 4. UPDATE - Update user
print("\n=== UPDATE USER ===")
updated = client.table("users").update({
    "name": "Alice Smith"
}).eq("id", 1).execute()
print(f"Updated {updated.count} user(s)")

# 5. DELETE - Remove user
print("\n=== DELETE USER ===")
deleted = client.table("users").delete().eq("id", 999).execute()
print(f"Deleted {deleted.count} user(s)")

# 6. Complex query
print("\n=== COMPLEX QUERY ===")
results = client.table("users") \
    .select("id", "name", "email", "age") \
    .gt("age", 21) \
    .lt("age", 65) \
    .like("email", "%@gmail.com") \
    .order_by("age", desc=False) \
    .limit(10) \
    .execute()
print(f"Found {results.count} users matching criteria")

# 7. Pagination
print("\n=== PAGINATION ===")
page_1 = client.table("users").select("*").limit(20).offset(0).execute()
page_2 = client.table("users").select("*").limit(20).offset(20).execute()
print(f"Page 1: {len(page_1.data)} users")
print(f"Page 2: {len(page_2.data)} users")

# 8. Utility methods
print("\n=== UTILITY METHODS ===")

# List all tables
tables = client.list_tables()
print(f"Tables in database: {tables}")

# Describe table schema
schema = client.describe_table("users")
print(f"Users table has {len(schema['columns'])} columns and {schema['row_count']} rows")

# Check API health
health = client.health()
print(f"API Status: {health['status']}")

# Close client
client.close()
print("\n✅ Done!")
