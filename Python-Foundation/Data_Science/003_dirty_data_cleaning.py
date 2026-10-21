import pandas as pd

df = pd.read_csv("Data_science/datasets/retail_store_sales.csv")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

print("--- Data Structure ---")
print(df.info())

print("\n--- Missing Values before Imputation  ---")
print(df.isnull().sum())

df["Discount Applied"] = df["Discount Applied"].fillna(0)
df_cleaned = df.dropna(subset=["Quantity", "Item", "Total Spent", "Price Per Unit"])

print("\n--- Missing Values after Imputation  ---")
print(df_cleaned.isnull().sum())
print(f"\nRemaining rows in dataset: {len(df_cleaned)}")
df_cleaned.to_csv("Data_Science/datasets/retail_store_sales_clean.csv", index=False)
