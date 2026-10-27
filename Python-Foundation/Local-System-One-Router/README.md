# Local AI Router and Code Generation API

A FastAPI experiment that runs a local Qwen 2.5 Instruct model for candidate scoring and code-generation requests. The model is loaded when the server starts, so the first startup downloads the model unless it is already cached.

## What is implemented

- `POST /v1/choice` scores the supplied options and returns a selected option with normalized scores.
- `POST /v1/noul` compares the model scores for “Yes” and “No”.
- `POST /v1/score` scores the rubric levels and returns a weighted score.
- `POST /v1/generate_code` returns generated code as plain text. The server does not execute the generated code.

These are experimental model outputs, not calibrated probabilities or reliable truth judgments. Review generated code before using it.

## Requirements

- Python 3.12 or newer
- A compatible PyTorch installation
- Sufficient memory for `Qwen/Qwen2.5-7B-Instruct` (GPU acceleration is optional)
- Network access on first run to download the model, unless it is already cached

## Run locally

```powershell
git clone https://github.com/rahuldegra1/Local-System-One-Router.git
Set-Location Local-System-One-Router
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn torch transformers numpy
uvicorn server:app --host 127.0.0.1 --port 8000
```

Example request:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/v1/choice `
  -ContentType application/json `
  -Body '{"state":"A user cannot access their account.","options":["billing","account access","shipping"]}'
```

The API has no authentication, rate limiting, or production deployment configuration. Keep it on a trusted local machine and do not expose it to an untrusted network.
