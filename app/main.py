from fastapi import FastAPI

from app.core.security import setup_middleware
from app.utils.logger import setup_logging

from app.api.routers.auth_router import router as auth_router
from app.api.routers.task_router import router as task_router
from app.api.routers.task_analytics_router import router as analytics_router
from app.api.routers.failed_task_router import router as failed_router
from app.api.routers.user_router import router as user_router

app = FastAPI(title="Production FastAPI Backend")

# middleware + logging
setup_middleware(app)
setup_logging()

# 🔥 NO PREFIXES (IMPORTANT FOR TESTS)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(analytics_router)
app.include_router(failed_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "API is running"}