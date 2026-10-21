import kaggle
import pandas as pd
import os

# 1. Define the Kaggle dataset path (Author/Dataset-Name)
dataset = "yasserh/titanic-dataset"
download_path = "./data"

# 2. Programmatically download the dataset
print(f"Downloading {dataset} from Kaggle...")
kaggle.api.dataset_download_files(dataset, path=download_path, unzip=True)

# 3. Find the downloaded CSV and load it into Pandas
# (Assuming the unzipped file is named Titanic-Dataset.csv)
csv_file = os.path.join(download_path, "Titanic-Dataset.csv")

print("Loading data into Pandas...")
df = pd.read_csv(csv_file)

# 4. Prove it works by printing the shape and the first 5 rows
print(f"Dataset Shape: {df.shape}")
print(df.head())

# 5. Data Analysis: Survival Rates using .groupby()
print("\n--- Survival Rates ---")

# Group by Gender
gender_survival = df.groupby("Sex")["Survived"].mean() * 100
print("\nBy Gender (%):")
print(gender_survival.round(2))

# Group by Ticket Class (1st, 2nd, 3rd)
class_survival = df.groupby("Pclass")["Survived"].mean() * 100
print("\nBy Ticket Class (%):")
print(class_survival.round(2))

# Group by Both Class and Gender
combo_survival = df.groupby(["Pclass", "Sex"])["Survived"].mean() * 100
print("\nBy Class and Gender (%):")
print(combo_survival.round(2))
