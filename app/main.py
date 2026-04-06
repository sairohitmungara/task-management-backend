from fastapi import FastAPI
from app.routers import routes

app = FastAPI()

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}
