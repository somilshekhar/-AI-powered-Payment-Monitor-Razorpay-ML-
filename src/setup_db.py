from .db import Base, engine
from . import db as _db  # noqa
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created.")
