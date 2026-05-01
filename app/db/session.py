from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

DATABASE_URL = "sqlite:///./test.db"  # change if using postgres

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        