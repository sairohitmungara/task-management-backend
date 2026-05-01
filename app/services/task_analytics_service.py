from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.task import Task


def get_task_analytics(db: Session, user_id: int):
    result = db.query(
        func.count(Task.id).label("total_tasks"),
        func.sum(case((Task.is_completed == True, 1), else_=0)).label("completed_tasks")
    ).filter(
        Task.user_id == user_id,
        Task.is_deleted == False
    ).first()

    total_tasks = result.total_tasks or 0
    completed_tasks = result.completed_tasks or 0
    pending_tasks = total_tasks - completed_tasks

    completion_percentage = 0.0
    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": round(completion_percentage, 2)
    }