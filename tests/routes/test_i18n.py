# tests/routes/test_i18n.py

from fastapi.testclient import TestClient

def test_get_translations_en(client: TestClient):
    response = client.get("/i18n/en")
    data = response.json()
    assert response.status_code == 200
    assert "navbar.home" in data 
    assert data["navbar.home"] == "Home"

def test_get_translations_es(client: TestClient):
    response = client.get("/i18n/es")
    data = response.json()
    assert response.status_code == 200
    assert "navbar.home" in data 
    assert data["navbar.home"] == "Inicio"

def test_get_non_existent_translation(client):
    response = client.get("/api/i18n/fr")
    assert response.status_code == 404
    