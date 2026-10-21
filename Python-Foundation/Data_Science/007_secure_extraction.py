import requests
import os
import pandas as pd
from dotenv import load_dotenv

# 1. Mount the hidden .env file and extract the key
load_dotenv()
secret_key = os.getenv("API_KEY")

# 2. Define the target
url = "https://api.fake-secure-server.com/v1/data"

# 3. Package the key into the request headers
headers = {"Authorization": f"Bearer {secret_key}", "Accept": "application/json"}

# 4. Execute the secure call
response = requests.get(url, headers=headers)

# 5. Intercept unauthorized failures immediately
if response.status_code == 401:
    print("Error: API Key is invalid or missing.")
elif response.status_code == 200:
    raw_data = response.json()
    df = pd.json_normalize(raw_data)
    print("Secure data extracted successfully.")
