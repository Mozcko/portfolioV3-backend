# tests/routes/test_technologies.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.services import technology_service
from src.schemas.technology import TechnologyCreate

def test_create_technology(client: TestClient, admin_auth_headers: dict, create_test_image):
    """Test creating a new technology."""
    test_icon = create_test_image("icon.png")
    response = client.post(
        "/technologies/",
        headers=admin_auth_headers,
        data={"name": "Python"},
        files={"icon": test_icon}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Python"
    assert "icon" in data
    assert data["icon"].endswith(".png")

def test_read_technologies(client: TestClient, db_session: Session, create_test_image):
    """Test reading a list of technologies."""
    tech_schema = TechnologyCreate(name="TestReadTech")
    filename, icon_bytes, _ = create_test_image()
    mock_icon_file = UploadFile(filename=filename, file=icon_bytes)
    technology_service.create_technology(db_session, tech_schema, mock_icon_file)

    response = client.get("/technologies/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(t["name"] == "TestReadTech" for t in data)

def test_read_technology(client: TestClient, db_session: Session, create_test_image):
    """Test reading a single technology by ID."""
    tech_schema = TechnologyCreate(name="SingleTech")
    filename, icon_bytes, _ = create_test_image()
    mock_icon_file = UploadFile(filename=filename, file=icon_bytes)
    tech = technology_service.create_technology(db_session, tech_schema, mock_icon_file)

    response = client.get(f"/technologies/{tech.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tech.id
    assert data["name"] == "SingleTech"

def test_update_technology(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a technology."""
    tech_schema = TechnologyCreate(name="OldName")
    filename, icon_bytes, _ = create_test_image()
    mock_icon_file = UploadFile(filename=filename, file=icon_bytes)
    tech = technology_service.create_technology(db_session, tech_schema, mock_icon_file)

    response = client.put(f"/technologies/{tech.id}", headers=admin_auth_headers, data={"name": "NewName"})
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"

def test_delete_technology(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test deleting a technology."""
    tech_schema = TechnologyCreate(name="ToDelete")
    filename, icon_bytes, _ = create_test_image()
    mock_icon_file = UploadFile(filename=filename, file=icon_bytes)
    tech = technology_service.create_technology(db_session, tech_schema, mock_icon_file)

    response = client.delete(f"/technologies/{tech.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/technologies/{tech.id}")
    assert get_response.status_code == 404

def test_unauthorized_create_technology(client: TestClient):
    """Test that creating a technology without auth fails."""
    response = client.post("/technologies/", data={"name": "Fail"})
    assert response.status_code == 401