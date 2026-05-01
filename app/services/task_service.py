from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.task import Task


# -------------------------
# GET ALL TASKS
# -------------------------
def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_deleted == False
    ).all()


# -------------------------
# GET SINGLE TASK
# -------------------------
def get_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id,
        Task.is_deleted == False
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# -------------------------
# CREATE TASK
# -------------------------
def create_task(db: Session, payload: dict, user_id: int):
    if not payload.get("title"):
        raise HTTPException(status_code=400, detail="Title is required")

    task = Task(
        title=payload.get("title"),
        description=payload.get("description"),
        user_id=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_completed": task.is_completed
    }


# -------------------------
# BULK CREATE
# -------------------------
def bulk_create_tasks(db: Session, payload: list, user_id: int):
    tasks = []

    for item in payload:
        if not item.get("title"):
            continue

        task = Task(
            title=item.get("title"),
            description=item.get("description"),
            user_id=user_id
        )

        db.add(task)
        tasks.append(task)

    db.commit()

    return [
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ]


# -------------------------
# UPDATE TASK
# -------------------------
def update_task(db: Session, task_id: int, payload: dict, user_id: int):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id,
        Task.is_deleted == False
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if "title" in payload:
        task.title = payload["title"]

    if "description" in payload:
        task.description = payload["description"]

    if "is_completed" in payload:
        task.is_completed = payload["is_completed"]

    db.commit()
    db.refresh(task)

    return task


# -------------------------
# DELETE TASK (SOFT DELETE)
# -------------------------
def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id,
        Task.is_deleted == False
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_deleted = True

    db.commit()

    return True


# -------------------------
# MARK ALL COMPLETE
# -------------------------
def mark_all_complete(db: Session, user_id: int):
    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_deleted == False
    ).all()

    count = 0

    for task in tasks:
        if not task.is_completed:
            task.is_completed = True
            count += 1

    db.commit()

    return count


# -------------------------
# ANALYTICS
# -------------------------
def get_task_analytics(db: Session, user_id: int):
    total = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_deleted == False
    ).count()

    completed = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_completed == True,
        Task.is_deleted == False
    ).count()

    pending = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_completed == False,
        Task.is_deleted == False
    ).count()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }