import pandas as pd

df = pd.read_csv("Data_science/datasets/retail_store_sales_clean.csv")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])


print("--- Data Structure ---")
print(df.info())

df["Transaction Month"] = df["Transaction Date"].dt.month
Total_revenue = df.groupby("Category")["Total Spent"].sum().sort_values(ascending=False)
print(Total_revenue)
print(df.head())
