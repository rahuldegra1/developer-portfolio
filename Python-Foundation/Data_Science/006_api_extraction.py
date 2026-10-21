import requests
import pandas as pd

# 1. The Endpoint
url = "https://fakestoreapi.com/products"

# 2. Defensive Call & Conversion
response = requests.get(url)
response.raise_for_status()
raw_data = response.json()

# 3. The Pandas Bridge
df = pd.json_normalize(raw_data)

# 4. Live Business Logic (Isolating top-rated items)
top_products = df[df["rating.rate"] >= 4.5]

# 5. Automated Client Deliverable
top_products.to_excel("Data_Science/datasets/Top_Rated_Products.xlsx", index=False)
