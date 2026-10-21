import requests

print("--- Welcome to the User Lookup Tool ---")

# 1. Ask the user for a number (instead of hardcoding it)
user_id = input("Enter a user ID to search for (1-10): ")

# 2. Inject that variable directly into the URL using an f-string (f"...")
url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

# 3. Make the GET request to the dynamic URL
response = requests.get(url)

# 4. Check if successful and print
if response.status_code == 200:
    user_data = response.json()

    print("\n--- User Information ---")
    print(f"Name: {user_data['name']}")
    print(f"Email: {user_data['email']}")
    print(f"City: {user_data['address']['city']}")
else:
    print(
        f"\nUser not found or failed to retrieve data. Status code: {response.status_code}"
    )
