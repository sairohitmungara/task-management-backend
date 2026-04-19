from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user.id)


@router.get("/")
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    status: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.get_tasks(
        db,
        current_user.id,
        skip,
        limit,
        status,
        search
    )


@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.get_task_by_id(db, task_id, current_user.id)


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.update_task(db, task_id, task, current_user.id)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.delete_task(db, task_id, current_user.id)