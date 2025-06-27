# tests/routes/test_auth.py

from fastapi.testclient import TestClient
from core.config import settings
from sqlalchemy.orm import Session
from models.user import User
from core.security import get_password_hash


def test_login_for_access_token(client: TestClient, admin_user: User):
    # Añade 'grant_type' aquí también
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
