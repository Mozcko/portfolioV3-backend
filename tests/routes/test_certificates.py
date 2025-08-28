import io
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.services import certificates_service
from src.schemas.certificate import CertificateCreate

def test_create_certificate(client: TestClient, admin_auth_headers: dict, create_test_image):
    """Test creating a new certificate."""
    test_image = create_test_image()

    response = client.post(
        "/certificates/",
        headers=admin_auth_headers,
        data={"title": "Certified Tester", "school": "Pytest University"},
        files={"file": test_image}
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Certified Tester"
    assert data["school"] == "Pytest University"
    assert "image_route" in data

def test_read_certificates(client: TestClient, db_session: Session, create_test_image):
    """Test reading a list of certificates."""
    # Create a certificate first
    cert_schema = CertificateCreate(title="Test Cert", school="Test School")    
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    certificates_service.create_certificate(db_session, cert_schema, mock_upload_file)

    response = client.get("/certificates/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(c["title"] == "Test Cert" for c in data)

def test_read_certificate(client: TestClient, db_session: Session, create_test_image):
    """Test reading a single certificate by ID."""
    cert_schema = CertificateCreate(title="Single Cert", school="ID School")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    cert = certificates_service.create_certificate(db_session, cert_schema, mock_upload_file)

    response = client.get(f"/certificates/{cert.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cert.id
    assert data["title"] == "Single Cert"

def test_read_nonexistent_certificate(client: TestClient):
    """Test reading a certificate that does not exist."""
    response = client.get("/certificates/9999")
    assert response.status_code == 404

def test_update_certificate(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a certificate's data."""
    cert_schema = CertificateCreate(title="Old Title", school="Old School")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    cert = certificates_service.create_certificate(db_session, cert_schema, mock_upload_file)

    response = client.put(
        f"/certificates/{cert.id}",
        headers=admin_auth_headers,
        data={"title": "New Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["school"] == "Old School" # Should remain unchanged

def test_update_certificate_image(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a certificate's image."""
    cert_schema = CertificateCreate(title="Image Update", school="School")
    filename, image_bytes, _ = create_test_image("old.jpg")
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    cert = certificates_service.create_certificate(db_session, cert_schema, mock_upload_file)
    old_image_route = cert.image_route

    new_image = create_test_image("new.jpg")
    response = client.put(
        f"/certificates/{cert.id}",
        headers=admin_auth_headers,
        files={"file": new_image}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["image_route"] != old_image_route

def test_delete_certificate(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test deleting a certificate."""
    cert_schema = CertificateCreate(title="To Be Deleted", school="Delete School")
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    cert = certificates_service.create_certificate(db_session, cert_schema, mock_upload_file)

    response = client.delete(f"/certificates/{cert.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/certificates/{cert.id}")
    assert response.status_code == 404