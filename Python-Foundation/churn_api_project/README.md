# Customer Churn Prediction API

A learning project that trains a scikit-learn pipeline on a small sample customer dataset and serves predictions through FastAPI. The included five-row dataset is only for exercising the workflow; its training-set score is not a meaningful measure of real-world performance.

## Requirements

- Python 3.12
- PostgreSQL
- Dependencies in `requirements.txt`

## Configure

Set `DATABASE_URL` to a PostgreSQL connection string and `JWT_SECRET_KEY` to a private random value with at least 32 characters. `MODEL_PATH` is optional and defaults to `best_churn_model.pkl`.

PowerShell example:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:5432/churn_db"
$secretBytes = New-Object byte[] 32
[Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($secretBytes)
$env:JWT_SECRET_KEY = [Convert]::ToBase64String($secretBytes)
```

Never commit `.env` files, real credentials, or untrusted pickle files. Copy `.env.example` as a reference; replace its placeholder values before use.

## Prepare the database and model

From the repository root, after PostgreSQL is running and the environment variables are set:

```powershell
python -m pip install -r requirements.txt
python -m src.db.loader
python -m src.ml.train
uvicorn src.api.main:app --reload
```

The loader creates the database tables and inserts the included sample CSV rows. Training creates a local model file, which is intentionally ignored by Git. The API reports a clear service-unavailable error until a model has been trained.

## Try the API

Open `http://127.0.0.1:8000/docs`, or request a demo token:

```powershell
$token = (Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/login?username=demo").access_token
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict/7590-VHVEG" -Headers @{ token = $token }
```

The login route issues a token for the supplied username; it is a demonstration mechanism, not user authentication. The sample is not production-ready and should not be used to make decisions about real customers.

## Tests

```powershell
python -m unittest discover -s tests -v
```
