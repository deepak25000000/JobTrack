def test_register_user(client): #this is for registration
    response = client.post(
        "/api/auth/register",

        json = {
        "username": "testuser",
            "email": "test@example.com",
            "password": "Password123"
        }
    )
    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"

    
#this is for login
def test_login_user(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "Password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "loginuser",
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Login successful"
    assert "access_token" in data

#this is for wrong password
def test_login_wrong_password(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "Password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "wrongpass",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    #this is for duplicate username
def test_duplicate_username(client):

    first_response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicate",
            "email": "one@example.com",
            "password": "Password123"
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicate",
            "email": "two@example.com",
            "password": "Password123"
        }
    )

    assert second_response.status_code == 409