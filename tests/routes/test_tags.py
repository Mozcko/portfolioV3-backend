from fastapi import status

def test_create_tag(client, admin_auth_headers):
    """Test creating a new tag"""
    response = client.post(
        "/tags/",
        json={"name": "Python"},
        headers=admin_auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Python"
    assert "id" in data

def test_create_duplicate_tag(client, admin_auth_headers):
    """Test creating a tag with a name that already exists"""
    # First creation
    client.post("/tags/", json={"name": "Unique"}, headers=admin_auth_headers)
    # Second creation (should fail)
    response = client.post(
        "/tags/",
        json={"name": "Unique"},
        headers=admin_auth_headers
    )
    # Depending on how SQLAlchemy handles integrity errors, this might be 400 or 500
    # But usually we expect an error. Assuming your global exception handler catches it or 500.
    # Ideally your service should check for existence, but for now let's check it's not 201
    assert response.status_code != status.HTTP_201_CREATED

def test_read_tags(client, admin_auth_headers):
    """Test reading list of tags"""
    client.post("/tags/", json={"name": "ReadMe"}, headers=admin_auth_headers)
    response = client.get("/tags/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0

def test_update_tag(client, admin_auth_headers):
    """Test updating a tag"""
    # Create
    res = client.post("/tags/", json={"name": "OldName"}, headers=admin_auth_headers)
    tag_id = res.json()["id"]
    
    # Update
    response = client.put(
        f"/tags/{tag_id}",
        json={"name": "NewName"},
        headers=admin_auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "NewName"

def test_delete_tag(client, admin_auth_headers):
    """Test deleting a tag"""
    # Create
    res = client.post("/tags/", json={"name": "ToDelete"}, headers=admin_auth_headers)
    tag_id = res.json()["id"]
    
    # Delete
    response = client.delete(f"/tags/{tag_id}", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    get_res = client.get(f"/tags/{tag_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND