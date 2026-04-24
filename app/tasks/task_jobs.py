from app.core.celery_worker import celery_app
import time


@celery_app.task(bind=True)
def long_task(self, name: str):
    total_steps = 5

    for i in range(total_steps):
        time.sleep(2)

        # update progress
        self.update_state(
            state="PROGRESS",
            meta={
                "current": i + 1,
                "total": total_steps,
                "percent": int(((i + 1) / total_steps) * 100)
            }
        )

    return f"Task completed for {name}"