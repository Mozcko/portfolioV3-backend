from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.services import jobs_service
from src.schemas.job import JobCreate

def test_create_job(client: TestClient, admin_auth_headers: dict, create_test_image):
    """Test creating a new job."""
    job_data = {
        "title": "Software Engineer",
        "start_date": "2023-01-01",
        "current_job": True
    }
    job_image = create_test_image()

    response = client.post(
        "/jobs/",
        headers=admin_auth_headers,
        data=job_data,
        files={"file": job_image}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Software Engineer"
    assert data["current_job"] is True

def test_read_jobs(client: TestClient, db_session: Session, create_test_image):
    """Test reading a list of jobs."""
    job_schema = JobCreate(title="Test Job", start_date="2022-01-01", current_job=False)
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    jobs_service.create_job(db_session, job_schema, mock_upload_file)

    response = client.get("/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_job(client: TestClient, db_session: Session, create_test_image):
    """Test reading a single job by ID."""
    job_schema = JobCreate(title="Single Job", start_date="2021-01-01", current_job=False)
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    job = jobs_service.create_job(db_session, job_schema, mock_upload_file)

    response = client.get(f"/jobs/{job.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job.id
    assert data["title"] == "Single Job"

def test_update_job(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test updating a job."""
    job_schema = JobCreate(title="Old Title", start_date="2020-01-01", current_job=False)
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    job = jobs_service.create_job(db_session, job_schema, mock_upload_file)

    response = client.put(
        f"/jobs/{job.id}",
        headers=admin_auth_headers,
        data={"title": "New Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"

def test_delete_job(client: TestClient, db_session: Session, admin_auth_headers: dict, create_test_image):
    """Test deleting a job."""
    job_schema = JobCreate(title="To Be Deleted", start_date="2019-01-01", current_job=False)
    filename, image_bytes, _ = create_test_image()
    mock_upload_file = UploadFile(filename=filename, file=image_bytes)
    job = jobs_service.create_job(db_session, job_schema, mock_upload_file)

    response = client.delete(f"/jobs/{job.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/jobs/{job.id}")
    assert get_response.status_code == 404