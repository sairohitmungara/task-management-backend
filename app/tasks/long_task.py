from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),  # 🔥 Auto retry for any exception
    retry_kwargs={"max_retries": 3},  # 🔥 Max 3 retries
    retry_backoff=True,  # 🔥 Exponential backoff (2,4,8 sec)
    retry_backoff_max=30,  # max wait cap
    retry_jitter=True,  # random delay (avoids spikes)
)
def long_task(self, name: str):
    try:
        total_steps = 5

        for i in range(total_steps):
            time.sleep(2)

            # 🔥 Simulate failure (for testing)
            if i == 2:
                raise ValueError("Simulated failure!")

            self.update_state(
                state="PROGRESS",
                meta={
                    "current": i + 1,
                    "total": total_steps,
                    "percent": int(((i + 1) / total_steps) * 100),
                },
            )

        return {
            "status": "SUCCESS",
            "message": f"Task completed for {name}",
        }

    except Exception as e:
        logger.error(f"Task failed: {str(e)}")

        # 🔥 This triggers retry
        raise self.retry(exc=e)