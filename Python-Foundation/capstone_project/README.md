# Year 2 Capstone API Prototype

A small FastAPI prototype for a customer-churn prediction API. It provides a health route and a sample prediction route whose risk calculation is simulated with a simple heuristic; it does not load a trained model or connect the API to the database service in the Compose file.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pydantic
uvicorn app:app --app-dir backend/app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API. This is a learning prototype, not a production prediction service.
