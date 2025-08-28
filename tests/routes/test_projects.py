# tests/routes/test_projects.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.services import technology_service, projects_service
from src.schemas.technology import TechnologyCreate
from src.schemas.project import ProjectCreate

def test_create_project(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test creating a new project."""
    # 1. Create a technology to link to
    tech_schema = TechnologyCreate(name="TestTech")
    filename, icon_bytes, _ = create_test_image("icon.png")
    mock_icon_file = UploadFile(filename=filename, file=icon_bytes)
    tech = technology_service.create_technology(db_session, tech_schema, mock_icon_file)

    # 2. Prepare project data
    project_data = {
        "title": "My Awesome Project",
        "description_en": "English description",
        "description_es": "Descripción en español",
        "technology_ids": str(tech.id)
    }
    project_image = create_test_image("project.jpg")

    # 3. Send request
    response = client.post(
        "/projects/",
        headers=admin_auth_headers,
        data=project_data,
        files={"image": project_image}
    )

    # 4. Assertions
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "My Awesome Project"
    assert len(data["technologies"]) == 1
    assert data["technologies"][0]["id"] == tech.id
    assert data["technologies"][0]["name"] == "TestTech"

def test_read_projects(client: TestClient, db_session: Session, create_test_image):
    """Test reading a list of projects."""
    # Create a project to ensure the list is not empty
    project_schema = ProjectCreate(title="List Project", description_en="en", description_es="es")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    projects_service.create_project(db_session, project_schema, mock_upload_file)

    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "List Project"

def test_read_project(client: TestClient, db_session: Session, create_test_image):
    """Test reading a single project by ID."""
    project_schema = ProjectCreate(title="Single Project", description_en="en", description_es="es")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    project = projects_service.create_project(db_session, project_schema, mock_upload_file)

    response = client.get(f"/projects/{project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project.id
    assert data["title"] == "Single Project"

def test_update_project(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a project."""
    project_schema = ProjectCreate(title="Old Project Title", description_en="en", description_es="es")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    project = projects_service.create_project(db_session, project_schema, mock_upload_file)

    response = client.put(
        f"/projects/{project.id}",
        headers=admin_auth_headers,
        data={"title": "New Project Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Project Title"

def test_delete_project(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test deleting a project."""
    project_schema = ProjectCreate(title="To Be Deleted", description_en="en", description_es="es")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    project = projects_service.create_project(db_session, project_schema, mock_upload_file)

    response = client.delete(f"/projects/{project.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/projects/{project.id}")
    assert get_response.status_code == 404