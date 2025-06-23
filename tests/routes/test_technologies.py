# tests/routes/test_technologies.py

from fastapi.testclient import TestClient
import io

def test_create_technology(client: TestClient, admin_auth_token: str):
    # Simular un archivo de imagen en memoria
    fake_image_bytes = b"fakedata"
    
    response = client.post(
        "/technologies/",
        headers={"Authorization": admin_auth_token},
        data={"name": "Docker", "color": "#2496ED"},
        files={"icon": ("docker.svg", io.BytesIO(fake_image_bytes), "image/svg+xml")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Docker"
    assert data["color"] == "#2496ED"
    assert "/static/images/" in data["icon"]

def test_read_technologies(client: TestClient):
    response = client.get("/technologies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_unauthorized_create_technology(client: TestClient):
    response = client.post(
        "/technologies/",
        data={"name": "Fail", "color": "#000000"},
        files={"icon": ("fail.png", b"data", "image/png")}
    )
    assert response.status_code == 401