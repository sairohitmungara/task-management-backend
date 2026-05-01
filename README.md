🚀 Production-Grade Task Management Backend (FastAPI)

A scalable and production-ready backend system built using FastAPI, featuring authentication, caching, asynchronous processing, and comprehensive test coverage.

---

## 🔥 Features

- 🔐 JWT Authentication (Login / Register)
- 👤 User-based Authorization
- 📝 Task CRUD APIs
- 📦 Bulk Task Creation
- 🗑️ Soft Delete & Restore
- ✅ Mark All Tasks Complete
- 📊 Task Analytics API
- ⚡ Redis Caching with cache invalidation
- 🔁 Celery Async Processing with retry mechanism
- ❌ Failed Task logging system
- 🚦 Rate Limiting using SlowAPI
- 🛡️ Global Exception Handling
- 📦 Standard API Response format
- 📜 Structured Logging
- ⚙️ Middleware (CORS, GZip, Security Headers)

---

## 🧠 Architecture

- Clean Architecture (Routers, Services, Models, Schemas)
- Dependency Injection (FastAPI Depends)
- Optimized DB queries using SQLAlchemy
- Proper DB session handling (including test isolation)

---

## 🛠️ Tech Stack

- Backend: FastAPI (Python)
- Database: PostgreSQL (production) / SQLite (testing)
- ORM: SQLAlchemy
- Authentication: JWT + OAuth2
- Caching: Redis
- Async Processing: Celery + Redis
- Testing: Pytest
- DevOps: Docker, Docker Compose

---

## 🧪 Testing

- Authentication tests
- Task API tests
- Failure scenarios
- Analytics validation

Run tests:

```bash
pytest -s
