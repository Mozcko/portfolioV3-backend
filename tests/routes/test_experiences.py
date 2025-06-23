# tests/routes/test_experiences.py

from fastapi.testclient import TestClient
import io

def test_create_experience(client: TestClient, admin_auth_token: str):
    fake_icon_bytes = b"experiencefakedata"
    
    experience_data = {
        "title": "Lead Test Engineer",
        "company_name": "QA Corp",
        "icon_bg": "#FFFFFF",
        "date": "2024 - Present",
        "points": "<li>Tested everything</li>"
    }
    
    response = client.post(
        "/experiences/",
        headers={"Authorization": admin_auth_token},
        data=experience_data,
        files={"icon": ("icon.png", io.BytesIO(fake_icon_bytes), "image/png")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Lead Test Engineer"
    assert data["company_name"] == "QA Corp"
    assert "/static/images/" in data["icon"]

def test_read_experiences(client: TestClient):
    response = client.get("/experiences/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)