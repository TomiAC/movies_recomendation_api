from fastapi.testclient import TestClient
from src.models import User

def test_register(client: TestClient):
    response = client.post("/auth/register", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user(client: TestClient, session):
    session.add(User(username="existinguser", hashed_password="somehashedpassword"))
    session.commit()
    response = client.post("/auth/register", data={"username": "existinguser", "password": "newpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_login(client: TestClient):
    client.post("/auth/register", data={"username": "testuser2", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser2", "password": "testpassword"})
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_login_incorrect_password(client: TestClient):
    client.post("/auth/register", data={"username": "testuser3", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser3", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}