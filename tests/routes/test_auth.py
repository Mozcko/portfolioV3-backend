# tests/routes/test_auth.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models.user import User


def test_login_for_access_token(client: TestClient, admin_user: User):
    """Test successful login and token generation."""
    login_data = {
        "grant_type": "password",
        "username": admin_user.username,
        "password": "testpassword",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_with_wrong_password(client: TestClient, admin_user: User):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": admin_user.username, 
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Usuario o contraseña incorrectos"}

def test_login_with_nonexistent_user(client: TestClient):
    """Test login with a user that does not exist."""
    response = client.post(
        "/auth/login",
        data={"grant_type": "password", "username": "nonexistent", "password": "password"},
    )
    assert response.status_code == 401

def test_read_users_me(client: TestClient, admin_auth_headers: dict, admin_user: User):
    response = client.get("/auth/me", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == admin_user.username
