from fastapi.testclient import TestClient

def test_get_popular_movies(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/recommendations/populars", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_recommend_by_content(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/recommendations/recommend/content/1", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert isinstance(response.json()[0], dict)

def test_recommend_hybrid(client: TestClient, rated_auth_token):
    headers = {"Authorization": f"Bearer {rated_auth_token}"}
    response = client.get("/recommendations/recommend/hybrid", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json(): # Check if the list is not empty
        assert isinstance(response.json()[0], dict)

def test_recommend(client: TestClient, rated_auth_token):
    headers = {"Authorization": f"Bearer {rated_auth_token}"}
    response = client.get("/recommendations/recommend", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if response.json(): # Check if the list is not empty
        assert isinstance(response.json()[0], dict)

def test_rate_movie(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    rating_data = {"movie_id": 2, "rating": 5.0}
    response = client.post("/recommendations/rate", headers=headers, json=rating_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Rating submitted successfully"}