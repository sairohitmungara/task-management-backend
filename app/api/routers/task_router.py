from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services import task_service
from app.utils.security import get_current_user

# Celery imports
from app.tasks.task_jobs import long_task
from app.core.celery_worker import celery_app

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ✅ CREATE TASK
@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user["user_id"])


# ✅ GET ALL TASKS
@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.get_tasks(db, current_user["user_id"])


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


# 🚀 START BACKGROUND TASK
@router.post("/long-task")
def run_long_task(name: str):
    task = long_task.delay(name)

    return {
        "task_id": task.id,
        "status": "Processing"
    }


# 🚀 TASK STATUS WITH PROGRESS
@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    if task.state == "PENDING":
        return {"status": "PENDING"}

    elif task.state == "PROGRESS":
        return {
            "status": "IN PROGRESS",
            "progress": task.info
        }

    elif task.state == "SUCCESS":
        return {
            "status": "SUCCESS",
            "result": task.result
        }

    elif task.state == "FAILURE":
        return {
            "status": "FAILED",
            "error": str(task.result)
        }

    return {"status": task.state}