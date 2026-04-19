from fastapi import FastAPI
from app.database import Base, engine

from app.routers import user_router, task_router

# 👇 THIS LINE CREATES TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(task_router.router)


@app.get("/")
def root():
    return {"message": "API is running"}