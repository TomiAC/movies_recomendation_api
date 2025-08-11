import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from src.models import Base, User
from src.database import get_db
from tests.database import override_get_db

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def session():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_register(client):
    response = client.post("/auth/register", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user(client, session):
    session.add(User(username="existinguser", hashed_password="somehashedpassword"))
    session.commit()
    response = client.post("/auth/register", data={"username": "existinguser", "password": "newpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_login(client):
    client.post("/auth/register", data={"username": "testuser", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_login_incorrect_password(client):
    client.post("/auth/register", data={"username": "testuser", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
