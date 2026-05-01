from pydantic import BaseModel


class TaskAnalyticsData(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_percentage: float