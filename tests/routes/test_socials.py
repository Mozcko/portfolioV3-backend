from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.services import socials_service
from src.schemas.social import SocialCreate

def test_create_social(client: TestClient, admin_auth_headers: dict, create_test_image):
    """Test creating a new social link."""
    social_data = {
        "name": "GitHub",
        "link": "https://github.com/user"
    }
    social_image = create_test_image()

    response = client.post(
        "/socials/",
        headers=admin_auth_headers,
        data=social_data,
        files={"file": social_image}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "GitHub"
    assert data["link"] == "https://github.com/user"

def test_read_socials(client: TestClient, db_session: Session, create_test_image):
    """Test reading a list of social links."""
    social_schema = SocialCreate(name="LinkedIn", link="https://linkedin.com")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    socials_service.create_social(db_session, social_schema, mock_upload_file)

    response = client.get("/socials/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_social(client: TestClient, db_session: Session, create_test_image):
    """Test reading a single social link by ID."""
    social_schema = SocialCreate(name="Twitter", link="https://twitter.com")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    social = socials_service.create_social(db_session, social_schema, mock_upload_file)

    response = client.get(f"/socials/{social.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == social.id
    assert data["name"] == "Twitter"

def test_update_social(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a social link."""
    social_schema = SocialCreate(name="Old Name", link="https://example.com")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    social = socials_service.create_social(db_session, social_schema, mock_upload_file)

    response = client.put(
        f"/socials/{social.id}",
        headers=admin_auth_headers,
        data={"name": "New Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"

def test_delete_social(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test deleting a social link."""
    social_schema = SocialCreate(name="To Be Deleted", link="https://deleteme.com")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    social = socials_service.create_social(db_session, social_schema, mock_upload_file)

    response = client.delete(f"/socials/{social.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/socials/{social.id}")
    assert get_response.status_code == 404