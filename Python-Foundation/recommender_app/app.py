import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Config
st.set_page_config(
    page_title="Book Recommender System", page_icon="📚", layout="centered"
)

st.title("📚 Smart Book Recommender System")
st.markdown(
    "Select a book you like, and our content-based machine learning model will recommend similar reads!"
)


# Sample dataset of books
@st.cache_data
def load_data():
    data = {
        "title": [
            "The Hobbit",
            "The Lord of the Rings",
            "Harry Potter and the Sorcerers Stone",
            "To Kill a Mockingbird",
            "1984",
            "Animal Farm",
            "Pride and Prejudice",
            "Jane Eyre",
        ],
        "genre": [
            "Fantasy Adventure Magic",
            "Epic Fantasy Adventure",
            "Fantasy Magic School",
            "Classic Drama Racism Justice",
            "Dystopian Totalitarianism Surveillance",
            "Political Satire Allegory Animals",
            "Classic Romance Society",
            "Gothic Romance Drama",
        ],
        "description": [
            "Bilbo Baggins embarks on an epic fantasy adventure with dwarves and a magical ring.",
            "Frodo Baggins sets out on an epic quest across middle earth to destroy the one ring.",
            "An orphaned boy discovers he is a wizard and attends a magical school of witchcraft.",
            "A gripping story of racial injustice and loss of innocence in the American South.",
            "A chilling dystopian novel depicting total government surveillance and thought control.",
            "Farm animals overthrow their human farmer, leading to a corrupt totalitarian society.",
            "A classic romantic comedy dealing with manners, upbringing, and marriage in British society.",
            "An orphaned governess falls in love with her brooding employer and uncovers dark secrets.",
        ],
    }
    return pd.DataFrame(data)


df = load_data()

# Compute TF-IDF Matrix and Cosine Similarity
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["genre"] + " " + df["description"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# User Selection UI
selected_book = st.selectbox("Choose a book you enjoy:", df["title"].values)

if st.button("Recommend Similar Books", type="primary"):
    # Find index of selected book
    idx = df[df["title"] == selected_book].index[0]

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top 3 recommendations (excluding itself)
    top_indices = [i[0] for i in sim_scores[1:4]]

    st.subheader("Top Recommended Reads for You:")
    for i in top_indices:
        rec_title = df.iloc[i]["title"]
        rec_genre = df.iloc[i]["genre"]
        st.success(f"📖 **{rec_title}** — *Genres: {rec_genre}*")
