# 📚 Content-Based Book Recommender System

## 1. Project Overview
This project is a machine learning-powered web application that recommends similar books based on text features such as genres and descriptions. It uses Natural Language Processing (NLP) techniques to compute textual similarity between books.

## 2. Tech Stack & Libraries
* **Python** (Core logic)
* **Pandas** (Data manipulation and structuring)
* **Scikit-Learn** (TF-IDF Vectorization & Cosine Similarity)
* **Streamlit** (Interactive web frontend UI)

## 3. Machine Learning Architecture
1. **Text Vectorization:** We combine the `genre` and `description` text fields and convert them into numerical vectors using `TfidfVectorizer` (Term Frequency-Inverse Document Frequency) to weigh important descriptive keywords.
2. **Similarity Metric:** We apply `cosine_similarity` to calculate the mathematical similarity score between every pair of books in the dataset.
3. **Recommendation Engine:** When a user selects a book, the system looks up its index, sorts all books by their cosine similarity score in descending order, and returns the top matching titles.

## 4. How to Run
1. Activate virtual environment: `.\venv\Scripts\activate`
2. Run the Streamlit app: `streamlit run app.py`