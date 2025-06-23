# tests/routes/test_technologies.py

from fastapi.testclient import TestClient
import io

def test_create_technology(client, admin_auth_token):
    tech_data = {
        "name": "New Tech",
        "image_url": "http://example.com/tech.png" # Asegúrate que tu schema no pida más campos
    }
    response = client.post(
        "/api/technologies/",
        headers={"Authorization": f"Bearer {admin_auth_token}"},
        json=tech_data
    )
    assert response.status_code == 200, response.text

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