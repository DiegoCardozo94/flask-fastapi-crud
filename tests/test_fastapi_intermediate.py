import pytest
from fastapi.testclient import TestClient
from fastapi_cruds.intermediate import app, fake_db

@pytest.fixture
def client():
    fake_db.clear()
    fake_db.update({
        1: {"name": "Item1", "description": "Desc1"},
        2: {"name": "Item2", "description": "Desc2"}
    })
    with TestClient(app) as client:
        yield client

# CREATE
def test_create_item_success(client):
    resp = client.post("/items/3", json={"name": "Item3", "description": "Desc3"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["message"] == "Item created"
    assert data["item"]["name"] == "Item3"
    assert 3 in fake_db

def test_create_existing_item(client):
    resp = client.post("/items/1", json={"name": "Duplicate"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Item already exists"

# READ
def test_read_existing_item(client):
    resp = client.get("/items/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["item_id"] == 1
    assert data["item"]["name"] == "Item1"

def test_read_nonexistent_item(client):
    resp = client.get("/items/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Item not found"

# UPDATE
def test_update_existing_item(client):
    resp = client.put("/items/1", json={"name": "UpdatedItem"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Item updated"
    assert fake_db[1]["name"] == "UpdatedItem"

def test_update_nonexistent_item_creates(client):
    resp = client.put("/items/10", json={"name": "NewItem"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["message"] == "Item created"
    assert fake_db[10]["name"] == "NewItem"

# DELETE
def test_delete_existing_item(client):
    resp = client.delete("/items/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Item 1 deleted"
    assert 1 not in fake_db

def test_delete_nonexistent_item(client):
    resp = client.delete("/items/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Item not found"

# LIST ALL
def test_list_items(client):
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "1" in data and "2" in data
