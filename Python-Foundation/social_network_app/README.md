# Social Network Analysis

A Streamlit demo that explores the Zachary Karate Club graph using NetworkX. It displays basic graph statistics, identifies the node with the highest degree centrality, and visualizes relationships.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit networkx matplotlib
streamlit run app.py
```

The example uses NetworkX's built-in graph dataset; no external data download is required.
