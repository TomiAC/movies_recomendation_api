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

@pytest.fixture(scope="session")
def test_user(client):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/auth/register", data=user_data)
    if response.status_code == 400:
        # User already exists, ignore
        pass
    return user_data

@pytest.fixture(scope="session")
def auth_token(client, test_user):
    response = client.post("/auth/token", data=test_user)
    return response.json()["access_token"]

@pytest.fixture(scope="session")
def rated_auth_token(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    rating_data = {"movie_id": 1, "rating": 5.0}
    response = client.post("/recommendations/rate", headers=headers, json=rating_data)
    assert response.status_code == 200
    return auth_token

def test_get_popular_movies(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/recommendations/populars", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_recommend_by_content(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/recommendations/recommend/content/1", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)

def test_recommend_hybrid(client, rated_auth_token):
    headers = {"Authorization": f"Bearer {rated_auth_token}"}
    response = client.get("/recommendations/recommend/hybrid", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json(): # Check if the list is not empty
        assert isinstance(response.json()[0], dict)

def test_recommend(client, rated_auth_token):
    headers = {"Authorization": f"Bearer {rated_auth_token}"}
    response = client.get("/recommendations/recommend", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json(): # Check if the list is not empty
        assert isinstance(response.json()[0], dict)

def test_rate_movie(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    rating_data = {"movie_id": 1, "rating": 5.0}
    response = client.post("/recommendations/rate", headers=headers, json=rating_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Rating submitted successfully"}
