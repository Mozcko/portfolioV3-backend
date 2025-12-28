import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

pytestmark = pytest.mark.skip("CV service is currently deactivated")

def test_download_cv(client: TestClient):
    """Test downloading the CV PDF."""
    # We test for 'es' but 'en' should work the same
    response = client.get("/cv/download/es")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in response.headers["content-disposition"]

def test_upload_cv(client: TestClient, admin_auth_headers: dict):
    """Test uploading a new CV markdown file."""
    fake_md_content = b"# New CV"
    fake_md_file = ("cv_es.md", io.BytesIO(fake_md_content), "text/markdown")

    response = client.put(
        "/cv/upload/es",
        headers=admin_auth_headers,
        files={"file": fake_md_file}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "CV for language 'es' updated successfully."}

def test_upload_cv_unauthorized(client: TestClient):
    """Test that uploading a CV without auth fails."""
    fake_md_content = b"# New CV"
    fake_md_file = ("cv_es.md", io.BytesIO(fake_md_content), "text/markdown")
    response = client.put("/cv/upload/es", files={"file": fake_md_file})
    assert response.status_code == 401

def test_download_cv_file_not_found(client: TestClient):
    """Test downloading a CV when the source file is missing."""
    # Patch the 'exists' method to simulate a missing file
    with patch("pathlib.Path.exists", return_value=False):
        response = client.get("/cv/download/en")
        assert response.status_code == 404