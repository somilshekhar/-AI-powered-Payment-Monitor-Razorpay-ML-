# AI-Powered Payment Monitoring System (Razorpay Integration)

A real-world, internship-ready project that combines live payment tracking, payment failure prediction, and fraud detection using Razorpay APIs and pre-trained ML models.

## Quickstart (Local Dev)

1) Open in VS Code.
2) Create a virtual environment and install deps:
```
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```
3) Copy `.env.example` → `.env` and fill Razorpay Test keys + DB URL.
4) Initialize DB and run first ingest + predict:
```
python -m src.setup_db
python -m src.ingest --count 50
python -m src.predict
```
5) Run API + dashboard:
```
uvicorn src.app:app --reload --port 8000
```
Visit: http://127.0.0.1:8000/dashboard

## Pre-trained Models

Put your pickled models in `src/models/`:
- failure_model.pkl
- fraud_model.pkl
- scaler.pkl (optional)

Code falls back to a simple baseline if models are missing.
