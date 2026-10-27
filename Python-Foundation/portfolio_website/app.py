import streamlit as st

st.set_page_config(
    page_title="My Data Science Portfolio", page_icon="🚀", layout="wide"
)

# Header Section
st.title("👋 Hi, I'm a Machine Learning Engineer")
st.subheader(
    "Building production-ready ML systems, scalable APIs, and data-driven insights."
)

st.markdown("""
**Tech Stack:** Python, FastAPI, Docker, PostgreSQL, scikit-learn, MLflow, Streamlit, NetworkX
**Target Roles:** Freelance ML Engineer (Upwork), Software Engineering Intern
""")

st.divider()

# Projects Section
st.header("🛠️ Featured Projects")

col1, col2 = st.columns(2)

with col1:
    st.success("### 1. Enterprise ML Capstone API")
    st.markdown("""
    A production-grade machine learning REST API built to predict customer churn.
    * **Tech:** FastAPI, Docker, PostgreSQL, scikit-learn
    * **Features:** Containerized architecture, automated DB migrations, real-time inference.
    """)
    st.button("View on GitHub", key="capstone_btn")

with col2:
    st.info("### 2. Social Network Graph Analyzer")
    st.markdown("""
    An interactive tool exploring graph theory and centrality metrics.
    * **Tech:** Python, NetworkX, Matplotlib, Streamlit
    * **Features:** Calculates node influence, maps visual relationships.
    """)
    st.button("View on GitHub", key="graph_btn")

st.divider()

# Experience & Contact
st.header("📈 ML Experiment Tracking")
st.markdown(
    "I utilize **MLflow** for robust experiment tracking, ensuring reproducible model training and hyperparameter tuning across my machine learning pipelines."
)

st.header("📬 Let's Connect")
st.markdown(
    "Check out my [LinkedIn](#) or read my latest technical deep-dives on my [Markdown Learning Journal](#)."
)
