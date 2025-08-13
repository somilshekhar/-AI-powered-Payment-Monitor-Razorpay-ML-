import os, pickle
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import SessionLocal, Payment, Prediction
from .features import payment_to_features, vectorize, baseline_failure_prob, baseline_fraud_score
from .config import FAILURE_ALERT_THRESHOLD, FRAUD_ALERT_THRESHOLD
from .alerts import send_email_alert
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
def _load(p): 
    with open(p, "rb") as f: return pickle.load(f)
def load_models():
    failure_model = fraud_model = scaler = None
    for name in ["failure_model.pkl","fraud_model.pkl","scaler.pkl"]:
        path = os.path.join(MODELS_DIR, name)
        if os.path.exists(path):
            try:
                obj = _load(path)
                if name=="failure_model.pkl": failure_model = obj
                elif name=="fraud_model.pkl": fraud_model = obj
                else: scaler = obj
                logger.info(f"Loaded {name}")
            except Exception as e:
                logger.warning(f"Failed to load {name}: {e}")
    return failure_model, fraud_model, scaler
def predict_row(feat, failure_model, fraud_model, scaler):
    x = [vectorize(feat)]
    if scaler is not None:
        try: x = scaler.transform(x)
        except Exception: pass
    if failure_model is not None and hasattr(failure_model, "predict_proba"):
        try: fp = float(failure_model.predict_proba(x)[0][-1])
        except Exception: fp = baseline_failure_prob(feat)
    else: fp = baseline_failure_prob(feat)
    if fraud_model is not None:
        try:
            if hasattr(fraud_model, "decision_function"):
                raw = float(fraud_model.decision_function(x)[0]); fr = (raw+1.0)/2.0
            elif hasattr(fraud_model, "score_samples"):
                raw = -float(fraud_model.score_samples(x)[0]); fr = 1.0 / (1.0 + pow(2.71828, -raw))
            else: fr = baseline_fraud_score(feat)
        except Exception: fr = baseline_fraud_score(feat)
    else: fr = baseline_fraud_score(feat)
    flags = []
    if fp >= FAILURE_ALERT_THRESHOLD: flags.append("HIGH_FAILURE_RISK")
    if fr >= FRAUD_ALERT_THRESHOLD: flags.append("FRAUD_SUSPECT")
    return fp, fr, ",".join(flags)
def main():
    failure_model, fraud_model, scaler = load_models()
    session: Session = SessionLocal()
    q = select(Payment).order_by(Payment.rzp_created_at.desc()).limit(200)
    payments = session.execute(q).scalars().all()
    created = alerts = 0
    for pay in payments:
        feat = payment_to_features(pay.raw or {})
        fp, fr, flags = predict_row(feat, failure_model, fraud_model, scaler)
        pred = Prediction(payment_id=pay.id, failure_prob=fp, fraud_score=fr, flags=flags)
        session.add(pred); created += 1
        if "HIGH_FAILURE_RISK" in flags or "FRAUD_SUSPECT" in flags:
            alerts += 1
            try:
                send_email_alert(subject=f"[Monitor] Alert for {pay.id}",
                                 body=f"Payment: {pay.id}\nStatus: {pay.status}\nAmount: {pay.amount}\nFailureProb: {fp:.2f}\nFraudScore: {fr:.2f}\nFlags: {flags}")
            except Exception as e: logger.warning(f"Alert failed: {e}")
    session.commit(); session.close()
    logger.success(f"Saved {created} predictions; alerts sent: {alerts}")
if __name__ == "__main__": main()
