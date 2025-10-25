import pytest
from fastapi.testclient import TestClient
from fastapi_cruds.advanced import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_item(client):
    resp = client.post("/items/1", json={"name": "Item1", "description": "Desc1"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "success"
    assert data["message"] == "Item created"
    assert data["data"]["name"] == "Item1"

def test_create_item_existing(client):
    client.post("/items/2", json={"name": "Item2"})
    resp = client.post("/items/2", json={"name": "Item2"})
    assert resp.status_code == 400
    data = resp.json()
    assert data["status"] == "error"
    assert "already exists" in data["message"]

def test_read_item(client):
    client.post("/items/3", json={"name": "Item3"})
    resp = client.get("/items/3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["data"]["name"] == "Item3"

def test_read_item_not_found(client):
    resp = client.get("/items/999")
    assert resp.status_code == 404
    data = resp.json()
    assert data["status"] == "error"
    assert "not found" in data["message"]

def test_list_items(client):
    client.post("/items/4", json={"name": "Item4"})
    client.post("/items/5", json={"name": "Item5"})
    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "4" in data["data"] and "5" in data["data"]

def test_list_items_with_filter(client):
    client.post("/items/6", json={"name": "SpecialItem"})
    client.post("/items/7", json={"name": "OtherItem"})
    resp = client.get("/items", params={"name": "Special"})
    data = resp.json()
    assert resp.status_code == 200
    assert data["status"] == "success"
    assert "6" in data["data"]
    assert "7" not in data["data"]
    for item in data["data"].values():
        assert "Special" in item["name"]

def test_update_item(client):
    client.post("/items/8", json={"name": "OldName"})
    resp = client.put("/items/8", json={"name": "NewName"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"]["name"] == "NewName"
    assert data["status"] == "success"

def test_update_item_create_new(client):
    resp = client.put("/items/9", json={"name": "CreatedViaPut"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["data"]["name"] == "CreatedViaPut"
    assert data["status"] == "success"

def test_delete_item(client):
    client.post("/items/10", json={"name": "ToDelete"})
    resp = client.delete("/items/10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "deleted" in data["message"]

def test_delete_item_not_found(client):
    resp = client.delete("/items/9999")
    assert resp.status_code == 404
    data = resp.json()
    assert data["status"] == "error"
    assert "not found" in data["message"]

@pytest.mark.parametrize("item_id", [9999])
def test_http_exception_handler(client, item_id):
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404
    data = resp.json()
    assert data["status"] == "error"
    assert "not found" in data["message"]
