from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user_router, task_router
from app.core.cache import init_cache   # ✅ ADDED

# 🔹 CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔹 ROUTERS
app.include_router(user_router.router)
app.include_router(task_router.router)

# 🔹 STARTUP EVENT (ADDED SAFELY)
@app.on_event("startup")
async def startup():
    await init_cache()

# 🔹 ROOT API
@app.get("/")
def root():
    return {"message": "API is running"}