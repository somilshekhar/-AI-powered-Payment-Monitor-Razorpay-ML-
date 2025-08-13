import argparse
from loguru import logger
from sqlalchemy.exc import IntegrityError
from .razclient import fetch_payments
from .db import SessionLocal, Payment
def upsert_payment(session, p):
    pay = Payment(
        id=p.get("id"),
        amount=p.get("amount"),
        currency=p.get("currency"),
        status=p.get("status"),
        method=p.get("method"),
        email=p.get("email"),
        contact=p.get("contact"),
        international=p.get("international"),
        fee=p.get("fee"),
        tax=p.get("tax"),
        error_code=p.get("error_code"),
        error_description=(p.get("error_reason") or p.get("error_description")),
        rzp_created_at=p.get("created_at"),
        raw=p
    )
    try:
        session.merge(pay)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
def main(count: int):
    logger.info(f"Fetching last {count} payments from Razorpay...")
    data = fetch_payments(count=count, skip=0)
    items = data.get("items", [])
    logger.info(f"Fetched {len(items)} payments")
    session = SessionLocal()
    n = 0
    for p in items:
        if upsert_payment(session, p): n += 1
    session.close()
    logger.success(f"Ingested/updated {n} payments.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()
    main(args.count)
