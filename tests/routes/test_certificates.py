import io
from fastapi.testclient import TestClient
from PIL import Image

def test_create_certificate(client: TestClient, admin_auth_token: str):
    # Crea una imagen de 1x1 pixel en memoria
    fake_image_bytes = io.BytesIO()
    image = Image.new('RGB', (1, 1))
    image.save(fake_image_bytes, 'jpeg')
    fake_image_bytes.seek(0) # Regresa al inicio del stream

    response = client.post(
        "/certificates/",
        headers={"Authorization": admin_auth_token},
        data={"title": "Certified Tester", "school": "Pytest University"},
        # Pasa los bytes de la imagen real
        files={"file": ("test_cert.jpg", fake_image_bytes, "image/jpeg")}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Certified Tester"

def test_read_certificates(client: TestClient):
    response = client.get("/certificates/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)