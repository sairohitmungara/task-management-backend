from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_user
from app.services import task_service


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return task_service.get_tasks(db, current_user.id)


@router.post("")
def create_task(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return task_service.create_task(db, payload, current_user.id)


@router.post("/bulk")
def bulk_create_tasks(payload: List[dict], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return task_service.bulk_create_tasks(db, payload, current_user.id)


@router.put("/mark-all-complete")
def mark_all_complete(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    updated = task_service.mark_all_complete(db, current_user.id)
    return {"updated_count": updated}


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return task_service.get_task(db, task_id, current_user.id)


@router.put("/{task_id}")
def update_task(task_id: int, payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return task_service.update_task(db, task_id, payload, current_user.id)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task_service.delete_task(db, task_id, current_user.id)
    return {"message": "Task deleted"}