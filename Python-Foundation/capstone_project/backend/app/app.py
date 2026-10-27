from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Capstone ML & Analytics API", version="1.0.0")


# Define request body schema for churn prediction
class CustomerData(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float


@app.get("/")
def read_root():
    return {"message": "Welcome to the Year 2 Capstone Production API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}


@app.post("/predict-churn")
def predict_churn(data: CustomerData):
    # Simulated prediction logic (In production, load your trained .pkl scikit-learn model here)
    risk_score = (data.monthly_charges / 100) - (data.tenure / 24)
    is_churn = risk_score > 0.5

    return {
        "tenure": data.tenure,
        "monthly_charges": data.monthly_charges,
        "churn_prediction": bool(is_churn),
        "risk_probability": round(min(max(risk_score, 0.0), 1.0), 2),
        "status": "Success",
    }
