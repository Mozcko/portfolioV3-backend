# tests/routes/test_i18n.py

from fastapi.testclient import TestClient

def test_get_translations_en(client: TestClient):
    response = client.get("/i18n/en")
    assert response.status_code == 200
    # Asumiendo que tu en.json tiene una clave "app_title"
    assert "app_title" in response.json()

def test_get_translations_es(client: TestClient):
    response = client.get("/i18n/es")
    assert response.status_code == 200
    # Asumiendo que tu es.json tiene una clave "app_title"
    assert "app_title" in response.json()

def test_get_non_existent_translation(client: TestClient):
    response = client.get("/i18n/fr") # 'fr' no existe
    assert response.status_code == 404
    assert response.json()["detail"] == "Language 'fr' not found"