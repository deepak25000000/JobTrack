#JOBTRACK API
Jobtrack Restfull API backend for manging and tracking job applications..
The project allows authenticated users to create, view, update, delete, search and filter their own job applications.

---

## Features:
- User registration
- User login
- Password hashing
- JWT authentication
- User-specific job ownership
- Create job applications
- Read job applications
- Update job applications
- Delete job applications
- Search jobs by role
- Filter by status
- Filter by company
- Filter by location
- Pagination
- Sorting
- Database migrations
- Automated testing 

## Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Flask-JWT-Extended
- Flask-Migrate
- Alembic
- pytest
- PostgreSQL for production

# Project Structure
```text
JobTrack/
│
├── app.py
├── extensions.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── job.py
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   └── job_routes.py
│
├── migrations/
│
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_jobs.py