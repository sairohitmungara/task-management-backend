from fastapi import FastAPI
from app.database import Base, engine

# ✅ UPDATED IMPORTS
from app.api.routers import user_router, task_router, task_status

from app.core.cache import init_cache

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router.router)
app.include_router(task_router.router)
app.include_router(task_status.router)