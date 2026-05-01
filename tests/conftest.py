import sys
import os

# Add project root to PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 🔥 Correct way to import FastAPI app
import importlib
main_module = importlib.import_module("app.main")
fastapi_app = main_module.app

from app.db.base_class import Base
from app.dependencies import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 🔥 IMPORTANT: register all models
import app.models.user
import app.models.task
import app.models.failed_task


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Override dependency
fastapi_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    with TestClient(fastapi_app) as c:
        yield c