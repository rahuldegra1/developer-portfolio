# Customer Segmentation Dashboard

An interactive Streamlit demo that uses K-Means clustering to group generated sample customers by annual income and spending score. Adjust the cluster count in the sidebar and view the resulting groups as a scatter plot.

## Stack

Python, Streamlit, pandas, NumPy, scikit-learn, Matplotlib, and Seaborn.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit pandas numpy scikit-learn matplotlib seaborn
streamlit run app.py
```

The app creates deterministic synthetic sample data; it does not require a customer dataset.
