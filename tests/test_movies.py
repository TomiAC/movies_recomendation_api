from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils import create_test_movie

def test_get_all_movies(client: TestClient, session: Session, auth_token: str):
    create_test_movie(session)

    response = client.get(
        "/movies",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["movies"]) == 1
    assert data["movies"][0]["title"] == "Test Movie"

def test_search_movie(client: TestClient, session: Session, auth_token: str):
    create_test_movie(session, title="Another Test Movie")

    response = client.get(
        "/movies/search?name=Another",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["movies"]) == 1
    assert data["movies"][0]["title"] == "Another Test Movie"

def test_search_movie_not_found(client: TestClient, session: Session, auth_token: str):
    create_test_movie(session)

    response = client.get(
        "/movies/search?name=NotFoun",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 0
    assert len(data["movies"]) == 0