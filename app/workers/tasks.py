from app.core.celery_worker import celery
from app.database import SessionLocal
from app.core.logger import logger

@celery.task(bind=True, max_retries=3)
def process_task(self, task_id: int):
    db = SessionLocal()
    try:
        logger.info(f"Processing task {task_id}")

        # your DB logic here

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Task failed: {str(e)}")
        raise self.retry(exc=e, countdown=10)

    finally:
        db.close()