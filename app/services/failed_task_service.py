from sqlalchemy.orm import Session
from app.models.failed_task import FailedTask


def save_failed_task(
    db: Session,
    task_id: str,
    error: str,
    data: dict,
    retry_count: int
):
    failed_task = FailedTask(
        task_id=task_id,
        error_message=error,   # ✅ IMPORTANT FIX
        data=data,
        retry_count=retry_count
    )

    db.add(failed_task)
    db.commit()
    db.refresh(failed_task)

    return failed_task