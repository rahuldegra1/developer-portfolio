import pandas as pd

df = pd.read_csv("Data_science/datasets/retail_store_sales_clean.csv")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])


print("--- Data Structure ---")
print(df.info())

df["Transaction Month"] = df["Transaction Date"].dt.month
Total_revenue = df.groupby("Category")["Total Spent"].sum().sort_values(ascending=False)
print(Total_revenue)
formatted_report = Total_revenue.reset_index()
formatted_report.to_excel(
    "Data_Science/datasets/Category_Revenue_Report.xlsx", index=False
)
print(df.head())
