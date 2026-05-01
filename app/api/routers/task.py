from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service
from app.core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return task_service.get_tasks(db, user.id)


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return task_service.create_task(db, task, user.id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = task_service.get_task(db, task_id, user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_service.update_task(db, task, task_data)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = task_service.get_task(db, task_id, user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_service.soft_delete_task(db, task)
    return {"message": "Task soft deleted"}


@router.post("/{task_id}/restore", response_model=TaskResponse)
def restore_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = task_service.restore_task(db, task_id, user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not deleted")

    return task