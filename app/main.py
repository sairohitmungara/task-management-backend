from fastapi import FastAPI
from app.routers import task_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task_router.router)
