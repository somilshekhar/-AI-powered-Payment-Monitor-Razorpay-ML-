import base64, requests
from typing import Dict, Any, Optional
from .config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
BASE_URL = "https://api.razorpay.com/v1"
def _auth_header() -> Dict[str, str]:
    token = base64.b64encode(f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()).decode()
    return {"Authorization": f"Basic {token}"}
def fetch_payments(count: int = 50, skip: int = 0, from_ts: Optional[int] = None, to_ts: Optional[int] = None) -> Dict[str, Any]:
    params = {"count": count, "skip": skip}
    if from_ts: params["from"] = from_ts
    if to_ts: params["to"] = to_ts
    r = requests.get(f"{BASE_URL}/payments", headers=_auth_header(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()
def fetch_payment_by_id(pay_id: str) -> Dict[str, Any]:
    r = requests.get(f"{BASE_URL}/payments/{pay_id}", headers=_auth_header(), timeout=30)
    r.raise_for_status()
    return r.json()
