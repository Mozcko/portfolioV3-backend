# tests/routes/test_experiences.py

import io
from fastapi.testclient import TestClient
from PIL import Image

def test_create_experience(client: TestClient, admin_auth_token: str):
    # Crea una imagen de 1x1 pixel para el icono
    fake_icon_bytes = io.BytesIO()
    image = Image.new('RGB', (1, 1))
    image.save(fake_icon_bytes, 'png')
    fake_icon_bytes.seek(0)

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
        # Pasa los bytes de la imagen real como el icono
        files={"icon": ("icon.png", fake_icon_bytes, "image/png")}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Lead Test Engineer"

def test_read_experiences(client: TestClient):
    response = client.get("/experiences/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)