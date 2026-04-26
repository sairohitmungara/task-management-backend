from sqlalchemy import Column, Integer, String, JSON
from app.database import Base


class FailedTask(Base):
    __tablename__ = "failed_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, index=True)
    error_message = Column(String)   # ✅ FIXED NAME
    data = Column(JSON)
    retry_count = Column(Integer)