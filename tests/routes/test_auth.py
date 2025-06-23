# tests/routes/test_auth.py

from fastapi.testclient import TestClient
from core.config import settings
from sqlalchemy.orm import Session
from models.user import User
from core.security import get_password_hash


def test_login_for_access_token(client, admin_user):
    # Envía los datos explícitamente como un formulario
    response = client.post(
        "/auth/login",
        data={"username": admin_user.username, "password": "testpassword"}
    )
    # Primero, verifica que el código de estado sea el correcto
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client, admin_user):
    response = client.post(
        "/auth/login",
        data={"username": admin_user.username, "password": "wrongpassword"}
    )
    # Para credenciales incorrectas, el código es 401 Unauthorized
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"