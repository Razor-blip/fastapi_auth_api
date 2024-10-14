from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "user1", "password": "password123", "full_name": "Test User"})
    assert response.status_code == 200
    assert response.json()["username"] == "user1"

def test_login_user():
    client.post("/register", json={"username": "user2", "password": "password123", "full_name": "Test User"})
    response = client.post("/login", data={"username": "user2", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_me():
    response = client.post("/login", data={"username": "user2", "password": "password123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "user2"
