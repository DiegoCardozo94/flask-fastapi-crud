import pytest
from flask_cruds.basic import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# CREATE
def test_create_user(client):
    resp = client.post("/users/1", json={"name": "Alice", "email": "alice@example.com"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["user_id"] == "1"
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"

# GET
def test_get_user(client):
    client.post("/users/2", json={"name": "John Doe", "email": "john@example.com"})
    resp = client.get("/users/2")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

# UPDATE
def test_update_user(client):
    client.post("/users/3", json={"name": "John Doe", "email": "john@example.com"})
    resp = client.put("/users/3", json={"name": "John Smith", "email": "johnsmith@example.com"})
    assert resp.status_code in (200, 204)
    resp_get = client.get("/users/3")
    data = resp_get.get_json()
    assert data["name"] == "John Smith"
    assert data["email"] == "johnsmith@example.com"

# DELETE
def test_delete_user(client):
    client.post("/users/4", json={"name": "Alice", "email": "alice@example.com"})
    resp = client.delete("/users/4")
    assert resp.status_code in (200, 204, 404)
    resp2 = client.get("/users/4")
    assert resp2.status_code == 404