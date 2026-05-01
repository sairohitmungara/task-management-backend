# 🚀 Production-Grade Task Management Backend (FastAPI)

A scalable backend system built using FastAPI with authentication, async processing, caching, and full test coverage.

---

## 🔥 Features

- 🔐 JWT Authentication (Login / Register)
- 👤 User-based Authorization
- 📝 Task CRUD APIs
- 📦 Bulk Task Creation
- 🗑️ Soft Delete & Restore
- ✅ Mark All Tasks Complete
- 📊 Task Analytics API
- ⚡ Redis Caching with Invalidation
- 🔁 Celery Async Processing with Retry
- ❌ Failed Task Logging System
- 🚦 Rate Limiting (SlowAPI)
- 🛡️ Global Exception Handling
- 📦 Standard API Response Format
- 📜 Structured Logging
- ⚙️ Middleware (CORS, GZip, Security Headers)

---

## 🧠 Architecture

- Clean Architecture (Routers, Services, Models, Schemas)
- Dependency Injection
- Optimized DB Queries (SQLAlchemy)
- Proper DB session handling (including test isolation)

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL / SQLite (testing)
- **ORM:** SQLAlchemy
- **Auth:** JWT + OAuth2
- **Caching:** Redis
- **Async Processing:** Celery + Redis
- **Testing:** Pytest
- **DevOps:** Docker, Docker Compose

---

## 🧪 Testing

- Authentication tests
- Task APIs tests
- Failure scenarios
- Analytics validation

```bash
pytest -s
