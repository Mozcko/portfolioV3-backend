# tests/routes/test_projects.py

from fastapi.testclient import TestClient
import io
import json

def test_create_project_with_technologies(client: TestClient, admin_auth_token: str):
    # 1. Primero, crea una tecnología para poder asociarla
    tech_response = client.post(
        "/technologies/",
        headers={"Authorization": admin_auth_token},
        data={"name": "FastAPI", "color": "#05998b"},
        files={"icon": ("fastapi.svg", io.BytesIO(b"icon"), "image/svg+xml")}
    )
    assert tech_response.status_code == 200
    tech_id = tech_response.json()["id"]

    # 2. Ahora, crea el proyecto asociando la tecnología por su ID
    fake_image_bytes = b"projectfakedata"
    tags_json = json.dumps([{"name": "Backend"}])
    tech_ids_json = json.dumps([tech_id])

    project_data = {
        "name": "Test Project",
        "interest": "High",
    }
    
    response = client.post(
        "/projects/",
        headers={"Authorization": admin_auth_token},
        data={**project_data, "tags": tags_json, "technology_ids": tech_ids_json},
        files={"image": ("project.jpg", io.BytesIO(fake_image_bytes), "image/jpeg")}
    )

    # 3. Verifica el resultado
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert len(data["technologies"]) == 1
    assert data["technologies"][0]["id"] == tech_id
    assert data["technologies"][0]["name"] == "FastAPI"
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "Backend"
    assert "/static/images/" in data["image_url"]