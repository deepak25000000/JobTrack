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

This is a complete, step-by-step guide to test every JobTrack API endpoint using [Postman](https://www.postman.com/).

### Step 0: Setup

1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/) (or use the web version).
2. Open Postman and click **Create a new Collection** → name it `JobTrack API`.
3. The **Base URL** for all requests is:
   ```
   https://jobtrack-827x.onrender.com
   ```
4. **Recommended:** Create an Environment for reusable variables.
   - Click **Environments** (left sidebar) → **Create Environment** → name it `JobTrack`.
   - Add these two variables and click **Save**:

   | Variable | Initial Value |
   |---|---|
   | `base_url` | `https://jobtrack-827x.onrender.com` |
   | `token` | *(leave empty for now — filled after login)* |

   - Select this environment from the environment dropdown (top-right corner) before testing.

---

### Step 1: Health Check (Optional)

First, verify the server is running.

- **Method:** `GET`
- **URL:** `{{base_url}}/health`
- **Headers:** None required.

**Steps in Postman:**
1. Click **New** → **HTTP Request** (or the ➕ tab).
2. Select `GET` from the method dropdown.
3. Paste `{{base_url}}/health` in the URL bar.
4. Click **Send**.

**Expected Response (Status `200 OK`):**
```json
{
  "status": "ok"
}
```

---

### Step 2: Register a New User

Create a new user account.

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/register`
- **Headers:** `Content-Type: application/json` (Postman sets this automatically when you pick JSON body)

**Steps in Postman:**
1. Open a new request tab.
2. Select `POST` and enter `{{base_url}}/api/auth/register`.
3. Go to the **Body** tab → select **raw** → choose **JSON** from the dropdown (right side).
4. Paste the following JSON:
   ```json
   {
     "username": "testuser",
     "email": "testuser@example.com",
     "password": "securepassword123"
   }
   ```
5. Click **Send**.

**Expected Response (Status `201 Created`):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com"
  }
}
```

**Possible Errors:**
| Status | Meaning | Cause |
|---|---|---|
| `400 Bad Request` | Missing `username`, `email`, or `password` | A required field is missing or body is not JSON |
| `409 Conflict` | `Username already exists` / `Email already exists` | User already registered — use a different username/email |

> **Tip:** Use a unique username/email each time, or simply proceed to login with the existing account.

---

### Step 3: Login and Get the Access Token

Log in to receive a JWT token, which is required for all job-related (protected) routes.

- **Method:** `POST`
- **URL:** `{{base_url}}/api/auth/login`

**Steps in Postman:**
1. Open a new request tab.
2. Select `POST` and enter `{{base_url}}/api/auth/login`.
3. Go to **Body** → **raw** → **JSON** and paste:
   ```json
   {
     "username": "testuser",
     "password": "securepassword123"
   }
   ```
4. Click **Send**.

**Expected Response (Status `200 OK`):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save the token (Important):**
1. **Copy** the entire value of `access_token` from the response.
2. Go to **Environments** → select your `JobTrack` environment.
3. Paste the token as the **Current Value** of the `token` variable → **Save**.

Now every protected request can use `Bearer {{token}}` automatically.

**Possible Errors:**
| Status | Meaning |
|---|---|
| `400 Bad Request` | `username` or `password` missing |
| `401 Unauthorized` | `Invalid username or password` |

---

### Step 4: Create a Job (Protected Route)

Add a new job application. All `/api/jobs` routes require the JWT token.

- **Method:** `POST`
- **URL:** `{{base_url}}/api/jobs`
- **Header:** `Authorization: Bearer {{token}}`

**Steps in Postman:**
1. Open a new request tab → select `POST` → enter `{{base_url}}/api/jobs`.
2. Go to the **Headers** tab and add:

   | Key | Value |
   |---|---|
   | `Authorization` | `Bearer {{token}}` |

   *(Alternatively, use the **Authorization** tab → Type: **Bearer Token** → paste `{{token}}`.)*
3. Go to **Body** → **raw** → **JSON** and paste:
   ```json
   {
     "role": "Software Engineer",
     "company": "Tech Corp",
     "location": "Remote",
     "status": "Applied"
   }
   ```
4. Click **Send**.

**Expected Response (Status `201 Created`):**
```json
{
  "id": 1,
  "role": "Software Engineer",
  "location": "Remote",
  "company": "Tech Corp",
  "status": "Applied",
  "user_id": 1
}
```

**Valid `status` values:** `Applied`, `Interview`, `Rejected`, `In-process`, `Selected`

**Possible Errors:**
| Status | Meaning |
|---|---|
| `400 Bad Request` | Missing required fields (`role`, `location`, `company`, `status`) or body is not JSON |
| `401 Unauthorized` | Missing/invalid/expired token — login again and update the `token` variable |

---

### Step 5: Get All Jobs (with Filters, Search, Sort & Pagination)

Fetch all jobs belonging to the logged-in user.

- **Method:** `GET`
- **URL:** `{{base_url}}/api/jobs`
- **Header:** `Authorization: Bearer {{token}}`

**Steps in Postman:**
1. Open a new request tab → select `GET` → enter `{{base_url}}/api/jobs`.
2. Add the `Authorization: Bearer {{token}}` header (same as Step 4).
3. Click **Send** — you will get an array of all your jobs.

**Using Query Parameters:**
Go to the **Params** tab and add key/value pairs (Postman builds the URL for you):

| Query Param | Description | Example | Notes |
|---|---|---|---|
| `status` | Filter by status | `Applied` | Exact match |
| `company` | Filter by company | `Tech Corp` | Exact match |
| `location` | Filter by location | `Remote` | Exact match |
| `search` | Search by job role | `engineer` | Partial, case-insensitive match |
| `page` | Page number | `2` | Must be ≥ 1 (default: `1`) |
| `limit` | Results per page | `5` | Must be between 1 and 100 (default: `10`) |
| `sort` | Sort field | `role` | Allowed: `id`, `role`, `company`, `location`, `status` (default: `id`) |
| `order` | Sort direction | `desc` | Allowed: `asc`, `desc` (default: `asc`) |

**Example — combined request:**
```
{{base_url}}/api/jobs?status=Applied&search=engineer&sort=role&order=desc&page=1&limit=5
```

**Expected Response (Status `200 OK`):**
```json
[
  {
    "id": 1,
    "role": "Software Engineer",
    "location": "Remote",
    "company": "Tech Corp",
    "status": "Applied",
    "user_id": 1
  }
]
```

**Possible Errors:**
| Status | Meaning |
|---|---|
| `400 Bad Request` | `Page number must be at least 1...`, `Limit must be between 1 and 100`, `Invalid sort field`, or `Order must be asc or desc` |
| `401 Unauthorized` | Missing/invalid token |

---

### Step 6: Get a Single Job by ID

- **Method:** `GET`
- **URL:** `{{base_url}}/api/jobs/1` (replace `1` with the actual job ID)
- **Header:** `Authorization: Bearer {{token}}`

**Steps in Postman:**
1. New request tab → `GET` → enter `{{base_url}}/api/jobs/1`.
2. Add the Authorization header.
3. Click **Send**.

**Expected Response (Status `200 OK`):**
```json
{
  "id": 1,
  "role": "Software Engineer",
  "location": "Remote",
  "company": "Tech Corp",
  "status": "Applied"
}
```

**Possible Errors:**
| Status | Meaning |
|---|---|
| `404 Not Found` | `Job not found` — wrong ID or the job belongs to another user |
| `401 Unauthorized` | Missing/invalid token |

---

### Step 7: Update a Job (PUT)

Update an existing job. **All four fields are required** — even if only one value changes.

- **Method:** `PUT`
- **URL:** `{{base_url}}/api/jobs/1`
- **Header:** `Authorization: Bearer {{token}}`

**Steps in Postman:**
1. New request tab → select `PUT` → enter `{{base_url}}/api/jobs/1`.
2. Add the Authorization header.
3. **Body** → **raw** → **JSON**:
   ```json
   {
     "role": "Senior Software Engineer",
     "company": "Tech Corp",
     "location": "Remote",
     "status": "Interview"
   }
   ```
4. Click **Send**.

**Expected Response (Status `200 OK`):**
```json
{
  "id": 1,
  "role": "Senior Software Engineer",
  "location": "Remote",
  "company": "Tech Corp",
  "status": "Interview"
}
```

**Possible Errors:**
| Status | Meaning |
|---|---|
| `400 Bad Request` | Missing fields, empty fields (`Fields cannot be empty`), or `Invalid status` (allowed: `Applied`, `Interview`, `Rejected`, `In-process`, `Selected`) |
| `404 Not Found` | `Job not found` |
| `401 Unauthorized` | Missing/invalid token |

---

### Step 8: Delete a Job

- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/jobs/1`
- **Header:** `Authorization: Bearer {{token}}`

**Steps in Postman:**
1. New request tab → select `DELETE` → enter `{{base_url}}/api/jobs/1`.
2. Add the Authorization header (no body needed).
3. Click **Send**.

**Expected Response (Status `200 OK`):**
```json
{
  "message": "Job deleted successfully"
}
```

**Possible Errors:**
| Status | Meaning |
|---|---|
| `404 Not Found` | `Job not found` — already deleted or belongs to another user |
| `401 Unauthorized` | Missing/invalid token |

---

### 📋 Endpoint Quick Reference

| # | Method | Endpoint | Auth | Purpose |
|---|---|---|---|---|
| 1 | `GET` | `/health` | ❌ | Health check |
| 2 | `POST` | `/api/auth/register` | ❌ | Register a new user |
| 3 | `POST` | `/api/auth/login` | ❌ | Login & get JWT token |
| 4 | `POST` | `/api/jobs` | ✅ | Create a job |
| 5 | `GET` | `/api/jobs` | ✅ | List/filter/search jobs |
| 6 | `GET` | `/api/jobs/:id` | ✅ | Get a single job |
| 7 | `PUT` | `/api/jobs/:id` | ✅ | Update a job |
| 8 | `DELETE` | `/api/jobs/:id` | ✅ | Delete a job |

---

### ⚠️ Troubleshooting

- **`401 Unauthorized` on job routes** — The token is missing, malformed, or expired. Re-run **Step 3 (Login)** and update the `token` environment variable. The header must be exactly `Bearer <token>` (note the space after `Bearer`).
- **`400 Request body must contain JSON data`** — You forgot to set the Body to **raw → JSON**, or the JSON is invalid (check for trailing commas or missing quotes).
- **`404 Not Found` on jobs** — The job ID doesn't exist, or it was created by a different user (each user only sees their own jobs).
- **Variables not resolving (`{{base_url}}` appears literally)** — Make sure the `JobTrack` environment is selected in the top-right dropdown and you clicked **Save** on the environment.
- **Render cold start** — The free service may take ~30–50 seconds to wake up on the first request. Wait and try again if the first request times out.

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