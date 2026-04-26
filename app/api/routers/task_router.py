from fastapi import APIRouter
from app.tasks.task_jobs import trigger_long_task

router = APIRouter()


@router.post("/tasks/long-task")
def run_long_task(data: dict):
    return trigger_long_task(data)