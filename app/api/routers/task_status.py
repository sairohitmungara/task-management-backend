from fastapi import APIRouter
from celery.result import AsyncResult
from app.celery_app import celery

router = APIRouter()


@router.get("/tasks/status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery)

    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }