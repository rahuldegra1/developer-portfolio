import pandas as pd
import joblib
from sqlalchemy import text
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src.db.database import get_engine
from src.ml.models import ChurnRandomForest


def run_pipeline():
    query = text("""
    SELECT u.gender, u.senior_citizen, s.tenure_months, s.monthly_charges, s.total_charges, s.churn
    FROM users u
    JOIN subscriptions s ON u.user_id = s.user_id
    """)
    df = pd.read_sql_query(query, get_engine())

    df["gender"] = df["gender"].apply(lambda x: 1 if x == "Female" else 0)

    X = df.drop("churn", axis=1)
    y = df["churn"]

    rf_model = ChurnRandomForest(n_estimators=50)

    pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", rf_model._model)])

    pipeline.fit(X, y)
    predictions = pipeline.predict(X)

    print("Training complete! Training-set accuracy:", accuracy_score(y, predictions))

    model_path = "best_churn_model.pkl"
    joblib.dump(pipeline, model_path)
    print(f"Pipeline saved to {model_path}")


if __name__ == "__main__":
    run_pipeline()
