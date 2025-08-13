from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from .config import DB_URL
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
class Payment(Base):
    __tablename__ = "payments"
    id = Column(String(64), primary_key=True)
    amount = Column(Integer)
    currency = Column(String(8))
    status = Column(String(32))
    method = Column(String(32))
    email = Column(String(255), nullable=True)
    contact = Column(String(64), nullable=True)
    international = Column(Boolean, nullable=True)
    fee = Column(Integer, nullable=True)
    tax = Column(Integer, nullable=True)
    error_code = Column(String(64), nullable=True)
    error_description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    rzp_created_at = Column(Integer, nullable=True)
    raw = Column(JSON)
    predictions = relationship("Prediction", back_populates="payment")
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String(64), ForeignKey("payments.id"))
    failure_prob = Column(Float)
    fraud_score = Column(Float)
    flags = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    payment = relationship("Payment", back_populates="predictions")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
