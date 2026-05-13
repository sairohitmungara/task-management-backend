# Production-Grade Task Management Backend

A scalable backend system built using FastAPI with authentication, caching, asynchronous task processing, and testing support.

## Features

- JWT Authentication (Login/Register)
- User-based Authorization
- Task CRUD APIs
- Bulk Task Creation
- Soft Delete and Restore
- Mark All Tasks Complete
- Task Analytics API
- Redis Caching with Cache Invalidation
- Celery Background Processing with Retry Mechanism
- Failed Task Logging
- Rate Limiting using SlowAPI
- Global Exception Handling
- Standardized API Responses
- Structured Logging
- Middleware Support (CORS, GZip, Security Headers)

## Architecture

- Clean Architecture (Routers, Services, Models, Schemas)
- Dependency Injection using FastAPI Depends
- Optimized Queries with SQLAlchemy
- Proper DB Session Handling
- Test Isolation Support

## Tech Stack

- FastAPI
- Python
- PostgreSQL
- SQLite (Testing)
- SQLAlchemy
- Redis
- Celery
- JWT Authentication
- Docker
- Pytest

## Testing

Covered:
- Authentication APIs
- Task APIs
- Failure Scenarios
- Analytics Validation

Run tests:

```bash
pytest -s
