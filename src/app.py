from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from .db import get_db, Payment, Prediction
app = FastAPI(title="AI Payment Monitor")
app.mount("/static", StaticFiles(directory=str(__file__).rsplit("/",1)[0] + "/static"), name="static")
templates = Jinja2Templates(directory=str(__file__).rsplit("/",1)[0] + "/templates")
@app.get("/health")
def health(): return {"ok": True}
@app.get("/payments")
def list_payments(db=Depends(get_db)):
    q = select(Payment).order_by(Payment.rzp_created_at.desc()).limit(100)
    rows = db.execute(q).scalars().all()
    return [{"id": r.id,"amount": r.amount,"currency": r.currency,"status": r.status,"method": r.method,"rzp_created_at": r.rzp_created_at} for r in rows]
@app.get("/predictions")
def list_predictions(db=Depends(get_db)):
    q = select(Prediction).order_by(Prediction.created_at.desc()).limit(100)
    rows = db.execute(q).scalars().all()
    return [{"payment_id": r.payment_id,"failure_prob": r.failure_prob,"fraud_score": r.fraud_score,"flags": r.flags,"created_at": r.created_at} for r in rows]
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db=Depends(get_db)):
    total = db.query(func.count(Payment.id)).scalar() or 0
    failed = db.query(func.count(Payment.id)).filter(Payment.status=="failed").scalar() or 0
    captured = db.query(func.count(Payment.id)).filter(Payment.status=="captured").scalar() or 0
    preds = db.query(func.count(Prediction.id)).scalar() or 0
    return templates.TemplateResponse("index.html", {"request": request,"total": total,"failed": failed,"captured": captured,"preds": preds})
