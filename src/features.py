from datetime import datetime, timezone
from typing import Dict, Any, List
def payment_to_features(p: Dict[str, Any]) -> Dict[str, float]:
    created = p.get("created_at")
    try:
        hour = datetime.fromtimestamp(int(created), tz=timezone.utc).hour if created else 0
    except Exception:
        hour = 0
    amt = float(p.get("amount") or 0.0) / 100.0
    method = (p.get("method") or "").lower()
    return {
        "amount_inr": amt,
        "is_card": 1.0 if method == "card" else 0.0,
        "is_upi": 1.0 if method == "upi" else 0.0,
        "is_netbanking": 1.0 if method == "netbanking" else 0.0,
        "is_wallet": 1.0 if method == "wallet" else 0.0,
        "hour": float(hour),
        "is_international": 1.0 if p.get("international") else 0.0,
        "has_error": 1.0 if p.get("error_code") else 0.0,
        "attempts": float(p.get("attempts") or 1.0),
    }
FEATURE_ORDER = ["amount_inr","is_card","is_upi","is_netbanking","is_wallet","hour","is_international","has_error","attempts"]
def vectorize(feat: Dict[str, float]) -> List[float]:
    return [float(feat.get(k, 0.0)) for k in FEATURE_ORDER]
def baseline_failure_prob(f: Dict[str, float]) -> float:
    prob = 0.05 + (0.15 if f.get("is_card") else 0.0) + (0.10 if f.get("has_error") else 0.0) + (0.10 if f.get("hour",0) in [0,1,2,3,4] else 0.0) + (0.10 if f.get("attempts",1)>2 else 0.0)
    return max(0.0, min(1.0, prob))
def baseline_fraud_score(f: Dict[str, float]) -> float:
    score = 0.05 + (0.15 if f.get("is_international") else 0.0) + (0.10 if f.get("amount_inr",0)>20000 else 0.0) + (0.10 if f.get("attempts",1)>3 else 0.0)
    return max(0.0, min(1.0, score))
