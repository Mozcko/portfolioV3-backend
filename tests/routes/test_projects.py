# tests/routes/test_projects.py

from fastapi.testclient import TestClient
import io
import json

def test_create_project_with_technologies(client, admin_auth_token):
    project_data = {
        "title": "New Test Project",
        "description": "A description for the test project",
        "image_url": "http://example.com/image.png",
        "project_url": "http://example.com/project",
        "tags": [],
        "technologies": []
    }
    # La URL correcta para la creación es "/api/projects/"
    response = client.post(
        "/api/projects/", # <-- Asegúrate que la URL sea esta
        headers={"Authorization": f"Bearer {admin_auth_token}"},
        json=project_data
    )
    assert response.status_code == 200, response.text