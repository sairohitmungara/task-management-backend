# Task Management Backend (FastAPI)

## Overview
This project is a backend system that allows users to securely manage tasks with authentication and strict ownership control.

## Features
- JWT-based user authentication
- Task CRUD operations
- Pagination and filtering
- Soft delete support
- User-specific task isolation
- Logging and error handling

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite

## Run Locally

pip install -r requirements.txt  
uvicorn app.main:app --reload  

## API Docs
http://127.0.0.1:8000/docs
