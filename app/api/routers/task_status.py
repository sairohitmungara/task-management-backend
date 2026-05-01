from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import User
from celery.result import AsyncResult
from app.celery_app import celery

router = APIRouter(prefix="/tasks", tags=["Task Status"])


@router.get("/status/{task_id}")
def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    task_result = AsyncResult(task_id, app=celery)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }