from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.failed_task import FailedTask

router = APIRouter(prefix="/failed-tasks", tags=["Failed Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_failed_tasks(db: Session = Depends(get_db)):
    tasks = db.query(FailedTask).all()
    return tasks
