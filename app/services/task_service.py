from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.utils.response import error_response
from app.utils.logger import logger


def create_task(db: Session, task_data: TaskCreate, user_id: int):
    logger.info(f"User {user_id} is creating a task")

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        owner_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Task {new_task.id} created by user {user_id}")
    return new_task


def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    status_filter: str = None,
    search: str = None
):
    logger.info(f"User {user_id} fetching tasks")

    query = db.query(Task).filter(
        Task.owner_id == user_id,
        Task.is_deleted == False
    )

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int, user_id: int):
    logger.info(f"User {user_id} requesting task {task_id}")

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.is_deleted == False
    ).first()

    if not task:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("Task not found")
        )

    if task.owner_id != user_id:
        logger.warning(f"Unauthorized access by user {user_id} for task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response("Not authorized")
        )

    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int):
    logger.info(f"User {user_id} updating task {task_id}")

    task = get_task_by_id(db, task_id, user_id)

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    logger.info(f"Task {task_id} updated by user {user_id}")
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    logger.info(f"User {user_id} deleting task {task_id}")

    task = get_task_by_id(db, task_id, user_id)

    task.is_deleted = True

    db.commit()

    logger.info(f"Task {task_id} soft-deleted by user {user_id}")
    return {"message": "Task deleted successfully"}