# tests/routes/test_certificates.py

from fastapi.testclient import TestClient
import io

def test_create_certificate(client: TestClient, admin_auth_token: str):
    fake_image_bytes = b"certificatefakedata"
    
    response = client.post(
        "/certificates/",
        headers={"Authorization": admin_auth_token},
        data={"title": "Certified Tester", "school": "Pytest University"},
        files={"file": ("test_cert.jpg", io.BytesIO(fake_image_bytes), "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Certified Tester"
    assert data["school"] == "Pytest University"
    assert "/static/images/" in data["image_route"]

def test_read_certificates(client: TestClient):
    response = client.get("/certificates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)