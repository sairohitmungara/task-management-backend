from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.task_schema import TaskCreate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskResponse)
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)

@router.get("/", response_model=list[TaskResponse])
def read_all(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse)
def read_one(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, task)

@router.delete("/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(db, task_id)