from fastapi import FastAPI
from app.database import Base, engine

from app.api.routers import user_router, task_router, task_status, failed_task_router

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router.router)
app.include_router(task_router.router)
app.include_router(task_status.router)
app.include_router(failed_task_router.router)