import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from src.database import get_db
from src.models import Base, User, Movie, Rating, Tag, Token
import warnings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_db():
    if os.path.exists("./test.db"):
        warnings.warn("test.db already exists, it will be removed")
        os.remove("./test.db")
        
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    os.remove("./test.db")

@pytest.fixture(scope="function")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_user(client: TestClient):
    user_data = {"username": "testuser_fixture", "password": "testpassword"}
    response = client.post("/auth/register", data=user_data)
    # It might fail if user already exists, but for a clean test run it's fine.
    # Consider adding cleanup or checking for existence if tests become flaky.
    return user_data

@pytest.fixture(scope="function")
def auth_token(client: TestClient, test_user):
    response = client.post("/auth/token", data=test_user)
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def rated_auth_token(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    rating_data = {"movie_id": 1, "rating": 5.0}
    # This might fail if movie with id 1 doesn't exist.
    # For now, assuming initial data loading handles this.
    response = client.post("/recommendations/rate", headers=headers, json=rating_data)
    assert response.status_code == 200
    return auth_token
