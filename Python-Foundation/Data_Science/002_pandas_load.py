import pandas as pd

df = pd.read_csv("Data_Science/datasets/sales_data.csv")


df["Date"] = pd.to_datetime(df["Date"])

print("--- Updated Data Types ---")
print(df.dtypes)

print("\n--- Total Revenue by Region ---")

region_sales = df.groupby("Region")["Revenue"].sum()
print(region_sales)

import matplotlib.pyplot as plt

print("\n--- Generating Chart ---")
# 3. Visualize the Data: Tell Pandas to draw a bar chart using our summarized data
region_sales.plot(kind="bar", color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])

# Add labels so the chart is readable
plt.title("Total Revenue by Region")
plt.ylabel("Revenue ($)")
plt.xlabel("Region")

# Pop open the actual graph window
plt.show()
