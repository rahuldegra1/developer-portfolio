import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Social Network Analysis", page_icon="🕸️", layout="centered"
)

st.title("🕸️ Social Network Analysis App")
st.markdown(
    "Analyze relationships, network graphs, and node influence using Graph Theory and NetworkX."
)


# Load a classic social network dataset (Zachary's Karate Club graph)
@st.cache_resource
def load_graph():
    return nx.karate_club_graph()


G = load_graph()

# Sidebar Metrics
st.sidebar.header("Network Statistics")
st.sidebar.metric(label="Total Members (Nodes)", value=G.number_of_nodes())
st.sidebar.metric(label="Total Connections (Edges)", value=G.number_of_edges())

# Calculate Centrality (Node Influence)
degree_cent = nx.degree_centrality(G)
top_influencer = max(degree_cent, key=degree_cent.get)

st.subheader("Key Network Insights")
st.success(
    f"🌟 **Most Influential Node (Highest Connections):** Member #{top_influencer} with {G.degree[top_influencer]} direct links."
)

# Visualization
st.subheader("Social Graph Visualization")
fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=700,
    edge_color="gray",
    linewidths=1,
    ax=ax,
)
st.pyplot(fig)
