# AI-Powered Payment Monitoring System (Razorpay Integration)

A real-world project that combines live payment tracking, payment failure prediction, and fraud detection using Razorpay APIs and pre-trained ML models.

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

# MIT License

Copyright (c) 2025 Somil Shekhar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
