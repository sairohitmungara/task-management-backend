from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services import task_service
from app.utils.security import get_current_user

from fastapi_cache.decorator import cache

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ✅ CREATE TASK
@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user["user_id"])


# ✅ GET ALL TASKS (CACHED)
@router.get("/")
@cache(expire=60)
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.get_tasks(db, current_user["user_id"])


# ✅ GET SINGLE TASK
@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = task_service.get_task(db, task_id, current_user["user_id"])
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# ✅ UPDATE TASK
@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_task = task_service.update_task(
        db, task_id, task, current_user["user_id"]
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


# ✅ DELETE TASK
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = task_service.delete_task(
        db, task_id, current_user["user_id"]
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}