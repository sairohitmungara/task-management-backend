from app.celery_app import celery
import logging

from app.database import SessionLocal
from app.services.failed_task_service import save_failed_task

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def long_task(self, data: dict):
    db = SessionLocal()

    try:
        logger.info(f"[START] Task ID: {self.request.id}")

        if data.get("fail"):
            raise Exception("Simulated failure triggered")

        return {
            "status": "success",
            "task_id": self.request.id,
            "data": data
        }

    except Exception as e:
        logger.error(f"[ERROR] Task ID: {self.request.id} | Error: {str(e)}")

        if self.request.retries >= (self.max_retries - 1):
            save_failed_task(
                db=db,
                task_id=self.request.id,
                error=str(e),
                data=data,
                retry_count=self.request.retries
            )

        # 🔥 FAST retry
        raise self.retry(exc=e, countdown=1, max_retries=3)

    finally:
        db.close()