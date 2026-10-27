import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Customer Segmentation", page_icon="📊", layout="centered"
)

st.title("📊 Customer Segmentation Dashboard")
st.markdown(
    "Using K-Means Unsupervised Machine Learning to cluster customers based on income and spending habits."
)


# Generate sample customer data
@st.cache_data
def load_data():
    np.random.seed(42)
    data = {
        "CustomerID": range(1, 201),
        "Age": np.random.randint(18, 70, size=200),
        "Annual_Income_k": np.random.randint(15, 140, size=200),
        "Spending_Score": np.random.randint(1, 100, size=200),
    }
    return pd.DataFrame(data)


df = load_data()

# Sidebar controls for K-Means
st.sidebar.header("Model Parameters")
k_clusters = st.sidebar.slider(
    "Select Number of Clusters (K)", min_value=2, max_value=6, value=4
)

# Apply KMeans
X = df[["Annual_Income_k", "Spending_Score"]]
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X)

# Display dataset sample
st.subheader("Customer Data Preview")
st.dataframe(df.head())

# Plot Clusters
st.subheader("Cluster Visualization")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    x="Annual_Income_k",
    y="Spending_Score",
    hue="Cluster",
    data=df,
    palette="viridis",
    s=100,
    ax=ax,
    legend="full",
)
plt.title("Customer Segments (Annual Income vs. Spending Score)")
plt.xlabel("Annual Income ($k)")
plt.ylabel("Spending Score (1-100)")
st.pyplot(fig)
