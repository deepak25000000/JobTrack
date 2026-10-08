#this is where we will test our backend 
'''
JWT
 ↓
User
 ↓
Job
 ↓
Ownership
'''
def register_and_login(client, username, email):

    client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": "Password123"
        }
    )

    return response.get_json()["access_token"]

def test_create_job(client):

    token = register_and_login(
        client,
        "jobuser",
        "job@example.com"
    )

    response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "role": "Backend Developer",
            "location": "Pune",
            "company": "Test Company",
            "status": "Applied"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["role"] == "Backend Developer"
    assert data["location"] == "Pune"
    assert data["company"] == "Test Company"
    assert data["status"] == "Applied"
    assert "user_id" in data

def test_get_jobs(client):

    token = register_and_login(
        client,
        "getuser",
        "get@example.com"
    )

    client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "role": "Python Developer",
            "location": "Pune",
            "company": "Company A",
            "status": "Applied"
        }
    )

    response = client.get(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["role"] == "Python Developer"

def test_get_jobs_without_token(client): #this is test is used for unauthenticated access

    response = client.get("/api/jobs")

    assert response.status_code == 401

#this test case is used for ownership of the particular job to a particular user 
#like user a has job1 and job2 and user b has job5 and job4 but user a cannot see user b job 
#bascially testing the authorization
def test_user_cannot_access_another_users_job(client):

    token_a = register_and_login(
        client,
        "usera",
        "usera@example.com"
    )

    token_b = register_and_login(
        client,
        "userb",
        "userb@example.com"
    )

    create_response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "role": "Backend Developer",
            "location": "Pune",
            "company": "Company A",
            "status": "Applied"
        }
    )

    assert create_response.status_code == 201

    job_id = create_response.get_json()["id"]

    response = client.get(
        f"/api/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404

def test_user_cannot_update_another_users_job(client):

    token_a = register_and_login(
        client,
        "updatea",
        "updatea@example.com"
    )

    token_b = register_and_login(
        client,
        "updateb",
        "updateb@example.com"
    )

    create_response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "role": "Backend Developer",
            "location": "Pune",
            "company": "Company A",
            "status": "Applied"
        }
    )

    job_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
        json={
            "role": "Hacked Developer",
            "location": "Mumbai",
            "company": "Hacked Company",
            "status": "Interview"
        }
    )

    assert response.status_code == 404

def test_user_cannot_delete_another_users_job(client):

    token_a = register_and_login(
        client,
        "deletea",
        "deletea@example.com"
    )

    token_b = register_and_login(
        client,
        "deleteb",
        "deleteb@example.com"
    )

    create_response = client.post(
        "/api/jobs",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "role": "Backend Developer",
            "location": "Pune",
            "company": "Company A",
            "status": "Applied"
        }
    )

    job_id = create_response.get_json()["id"]

    response = client.delete(
        f"/api/jobs/{job_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404

