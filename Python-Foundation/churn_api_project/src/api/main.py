import logging
import os
import time
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

import joblib
import jwt
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import text

from src.db.database import get_engine

logger = logging.getLogger(__name__)
app = FastAPI(title="Customer Churn Prediction API")
MODEL_PATH = Path(
    os.environ.get(
        "MODEL_PATH",
        Path(__file__).resolve().parents[2] / "best_churn_model.pkl",
    )
)
model = None


def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        logger.info(
            "Endpoint %s executed in %.4f seconds",
            func.__name__,
            time.perf_counter() - start,
        )
        return result

    return wrapper


def get_jwt_secret_key() -> str:
    secret_key = os.environ.get("JWT_SECRET_KEY")
    if not secret_key or len(secret_key) < 32:
        raise HTTPException(
            status_code=503,
            detail="Set JWT_SECRET_KEY to a random value of at least 32 characters.",
        )
    return secret_key


def get_model():
    global model
    if model is None:
        if not MODEL_PATH.is_file():
            raise HTTPException(
                status_code=503,
                detail="Model file not found. Train the model before requesting predictions.",
            )
        model = joblib.load(MODEL_PATH)
    return model


@app.post("/login")
def login(username: str):
    if not username.strip():
        raise HTTPException(status_code=400, detail="Username must not be empty.")
    token = jwt.encode(
        {
            "sub": username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        get_jwt_secret_key(),
        algorithm="HS256",
    )
    return {"access_token": token}


def verify_token(token: str | None = Header(default=None)) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token.")
    try:
        claims = jwt.decode(token, get_jwt_secret_key(), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    username = claims.get("sub")
    if not isinstance(username, str):
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    return username


@app.get("/predict/{customer_id}")
@log_execution_time
def predict_churn(customer_id: str, _username: str = Depends(verify_token)):
    query = text("""
        SELECT u.gender, u.senior_citizen, s.tenure_months,
               s.monthly_charges, s.total_charges
        FROM users u
        JOIN subscriptions s ON u.user_id = s.user_id
        WHERE u.customer_id = :customer_id
    """)
    df = pd.read_sql_query(
        query,
        get_engine(),
        params={"customer_id": customer_id},
    )

    if df.empty:
        raise HTTPException(status_code=404, detail="Customer not found in database.")

    df["gender"] = df["gender"].apply(lambda value: 1 if value == "Female" else 0)
    prediction = int(get_model().predict(df)[0])

    return {
        "customer_id": customer_id,
        "will_churn": bool(prediction),
    }
