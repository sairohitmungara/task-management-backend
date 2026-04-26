from app.tasks.long_task import long_task


def trigger_long_task(data: dict):
    task = long_task.delay(data=data)   # ✅ IMPORTANT FIX

    return {
        "task_id": task.id,
        "status": "processing"
    }