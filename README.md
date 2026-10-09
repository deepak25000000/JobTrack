# JobTrack API

JobTrack is a secure, RESTful API backend designed for managing and tracking job applications. It allows authenticated users to create, view, update, delete, search, and filter their own job applications efficiently.

**Live Backend URL:** [https://jobtrack-827x.onrender.com](https://jobtrack-827x.onrender.com)

---

## 🚀 Features

- **Authentication & Security:** User registration, login, password hashing, and JWT-based authentication. User-specific data isolation (users can access only their own jobs).
- **Job Management:** Complete CRUD operations (Create, Read, Update, Delete) for job applications.
- **Advanced Querying:** Search by job role, and filter by status, company, or location. Includes pagination and sorting.
- **Code Quality:** Automated testing (`pytest`) and database migrations (`Flask-Migrate`).

---

## 💻 Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database & ORM:** PostgreSQL (Production), SQLite (Local Development), Flask-SQLAlchemy, SQLAlchemy
- **Authentication:** Flask-JWT-Extended
- **Migrations:** Flask-Migrate (Alembic)
- **Testing:** pytest

---

## 🧪 API Testing Guide (via Postman)

You can easily test the API using [Postman](https://www.postman.com/) or any other API client. The base URL is `https://jobtrack-827x.onrender.com`.

### 1. User Creation (Register)
Create a new user account.
- **Endpoint:** `POST /api/auth/register`
- **Body (JSON):**
  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword123"
  }
  ```

### 2. User Login
Log in to get your access token for protected routes.
- **Endpoint:** `POST /api/auth/login`
- **Body (JSON):**
  ```json
  {
    "username": "testuser",
    "password": "securepassword123"
  }
  ```
- **Response:** You will receive an `access_token`. **Copy this token** for the next step.

### 3. Job Creation (Protected Route)
Add a new job application.
- **Endpoint:** `POST /api/jobs`
- **Headers:** 
  - `Authorization`: `Bearer <paste_your_access_token_here>`
- **Body (JSON):**
  ```json
  {
    "role": "Software Engineer",
    "company": "Tech Corp",
    "location": "Remote",
    "status": "Applied"
  }
  ```

---

## 📂 Project Structure

```text
JobTrack/
│
├── .github/
│   └── workflows/
│       └── tests.yml      # CI/CD pipeline for automated testing
├── migrations/            # Database migration scripts
├── models/                # Database models
│   ├── __init__.py
│   ├── job.py             # Job application model
│   └── user.py            # User model
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── auth_routes.py     # User registration and login routes
│   └── job_routes.py      # Job CRUD endpoints
├── tests/                 # Pytest test cases
│   ├── conftest.py        # Pytest fixtures
│   ├── test_auth.py       # Authentication tests
│   └── test_jobs.py       # Job endpoints tests
│
├── .env                   # Environment variables (DB URL, JWT Secret)
├── .gitignore             # Git ignore file
├── app.py                 # Main Flask application entry point
├── extensions.py          # Flask extensions setup
└── requirements.txt       # Project dependencies
```