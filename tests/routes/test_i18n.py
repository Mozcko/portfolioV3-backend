# tests/routes/test_i18n.py

from fastapi.testclient import TestClient
import json
from src.services import i18n_service

def test_get_translations_en(client: TestClient):
    """Test fetching English translations."""
    response = client.get("/i18n/en")
    data = response.json()
    assert response.status_code == 200
    assert "navbar.home" in data
    assert data["navbar.home"] == "Home"

def test_get_translations_es(client: TestClient):
    """Test fetching Spanish translations."""
    response = client.get("/i18n/es")
    data = response.json()
    assert response.status_code == 200
    assert "navbar.home" in data
    assert data["navbar.home"] == "Inicio"

def test_get_non_existent_translation(client: TestClient):
    """Test fetching a language that does not exist."""
    response = client.get("/i18n/fr")
    assert response.status_code == 404

def test_list_available_languages(client: TestClient):
    """Test listing all available languages."""
    response = client.get("/i18n/")
    assert response.status_code == 200
    data = response.json()
    assert "en" in data
    assert "es" in data

def test_update_language_file(client: TestClient, admin_auth_headers: dict):
    """Test updating a language file (protected endpoint)."""
    update_data = {"new.key": "New Value"}
    response = client.put(
        "/i18n/en",
        headers=admin_auth_headers,
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["new.key"] == "New Value"
    # Verify the original data is still there
    assert data["navbar.home"] == "Home"