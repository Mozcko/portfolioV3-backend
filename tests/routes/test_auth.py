# tests/routes/test_auth.py

from fastapi.testclient import TestClient
from src.core.config import settings
from sqlalchemy.orm import Session
from src.models.user import User
from src.core.security import get_password_hash

def test_login_for_access_token(client: TestClient, db_session: Session):
    # Crear un usuario de prueba
    password = settings.ADMIN_PASSWORD
    test_user = User(
        username=settings.ADMIN_USERNAME,
        email="test@example.com",
        hashed_password=get_password_hash(password)
    )
    db_session.add(test_user)
    db_session.commit()

    # Probar el login
    login_data = {"username": settings.ADMIN_USERNAME, "password": password}
    response = client.post("/auth/token", data=login_data)

    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def test_login_with_wrong_password(client: TestClient, db_session: Session):
    # Crear usuario
    test_user = User(
        username="wronguser",
        email="wrong@example.com",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(test_user)
    db_session.commit()

    # Probar login con contraseña incorrecta
    login_data = {"username": "wronguser", "password": "wrongpassword"}
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"