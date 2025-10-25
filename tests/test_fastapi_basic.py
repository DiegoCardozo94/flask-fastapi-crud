import pytest
from fastapi.testclient import TestClient
from fastapi_cruds.basic import app, fake_db

@pytest.fixture
def client():
    fake_db.clear()
    with TestClient(app) as client:
        yield client

# CREATE
def test_create_item(client):
    resp = client.post("/items/1", json={"name": "Item1", "description": "Desc1"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Item 1 created"
    assert data["item"]["name"] == "Item1"

def test_create_existing_item(client):
    client.post("/items/1", json={"name": "Item1", "description": "Desc1"})
    resp = client.post("/items/1", json={"name": "Duplicate", "description": "Desc2"})
    data = resp.json()
    assert data["message"] == "Item 1 already exists"
    assert data["item"]["name"] == "Item1"

# READ
def test_read_item(client):
    client.post("/items/2", json={"name": "Item2", "description": "Desc2"})
    resp = client.get("/items/2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["item"]["name"] == "Item2"

def test_read_nonexistent_item(client):
    resp = client.get("/items/999")
    data = resp.json()
    assert data["item"] is None

# UPDATE
def test_update_existing_item(client):
    client.post("/items/3", json={"name": "Item3", "description": "Desc3"})
    resp = client.put("/items/3", json={"name": "Updated", "description": "NewDesc"})
    data = resp.json()
    assert data["message"] == "Item 3 updated"
    assert data["item"]["name"] == "Updated"

def test_update_nonexistent_item(client):
    resp = client.put("/items/4", json={"name": "NewItem", "description": "Desc"})
    data = resp.json()
    assert data["message"] == "Item 4 created"
    assert data["item"]["name"] == "NewItem"

# DELETE
def test_delete_existing_item(client):
    client.post("/items/5", json={"name": "Item5", "description": "Desc5"})
    resp = client.delete("/items/5")
    data = resp.json()
    assert data["message"] == "Item 5 deleted"
    assert 5 not in fake_db

def test_delete_nonexistent_item(client):
    resp = client.delete("/items/999")
    data = resp.json()
    assert data["message"] == "Item 999 does not exist"
