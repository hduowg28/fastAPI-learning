# FastAPI Learning Journey

This repository documents my journey of learning FastAPI from the basics to building production-ready REST APIs.

The goal of this repository is not only to learn FastAPI syntax but also to understand how professional backend projects are organized.

use ``` uvicorn app.main:app --reload ``` to run the application

---

# Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- SQLite
- JWT Authentication
- Docker
- Redis
- Pytest

---

# Project Structure

```
app/
├── api/
├── core/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
└── main.py
```

---

# What I Learned

## API Layer

- Contains all API endpoints.
- Handles HTTP requests and responses.
- Does **not** contain business logic.

Example:

```python
@router.post("/")
def create_book(book: BookCreate):
    return book_service.create(book)
```

---

## Models

SQLAlchemy models map Python classes to database tables.

Example:

```python
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
```

---

## Schemas

Pydantic models are used to

- Validate request data
- Serialize responses
- Parse incoming data

Example

```python
class BookCreate(BaseModel):
    title: str
    price: float
```

---

## Services

Contains business logic.

Example

```python
def create_book(book):
    if book.quantity == 0:
        raise Exception("Book is out of stock")
```

---

## Repositories

Responsible for communicating with the database.

Example

```python
def get_book(db, id):
    return db.query(Book).filter(...).first()
```

Flow:

```
Service
    ↓
Repository
    ↓
Database
```

---

## Core

Shared components

- Database configuration
- JWT
- Settings
- Environment variables

---

## Utils

Utility functions

- Password hashing
- JWT encoding
- Pagination
- File upload
- Email sending

---

## Tests

Unit tests using Pytest

Examples

- test_book.py
- test_auth.py
- test_user.py

---

# Request Flow

```
Browser
    ↓
API Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Response

```
Database
    ↓
Repository
    ↓
Service
    ↓
API Router
    ↓
Browser
```

---

# Database

Development

```
FastAPI
    ↓
SQLite
```

Production

```
FastAPI
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

---

# Authentication

- Register
- Login
- JWT
- Refresh Token
- Role-based Authorization

Roles

- Admin
- Librarian
- Student

---

# Logging

```
logs/app.log
```

Example

```python
logger.info(...)
logger.error(...)
```

---

# Environment Variables

```
DATABASE_URL=
SECRET_KEY=
JWT_SECRET=
DEBUG=True
```

Sensitive information should never be hard-coded.

---

# Database Migration

Using Alembic

```bash
alembic init migrations
alembic revision --autogenerate
alembic upgrade head
```

---

# Testing

Using Pytest

- Login
- CRUD
- Permissions
- Database
- Authentication

---

# API Documentation

FastAPI automatically generates

- /docs
- /redoc

---

# Learning Roadmap

- [x] FastAPI Basics
- [ ] SQLAlchemy
- [ ] CRUD
- [ ] Authentication
- [ ] Docker
- [ ] Redis
- [ ] Testing
- [ ] Deployment