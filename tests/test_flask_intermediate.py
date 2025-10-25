import pytest
from flask.testing import FlaskClient
from flask_cruds.intermediate import app, fake_db

@pytest.fixture()
def client() -> FlaskClient:
    app.config["TESTING"] = True

    fake_db.clear()
    fake_db.update({
        "1": {"user_id": "1", "name": "John Doe", "email": "j@j.com"},
        "2": {"user_id": "2", "name": "Jane Smith", "email": "jane@x.com"}
    })

    with app.test_client() as client:
        yield client

# GET (Read)
def test_get_existing_user(client):
    resp = client.get("/users/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["user_id"] == "1"
    assert "name" in data
    assert "email" in data

def test_get_nonexistent_user_returns_404(client):
    resp = client.get("/users/999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert "User not found" in data["message"] or "User not found" in data.get("description", "")

# POST (Create)
def test_create_user_success(client):
    new_user = {"user_id": "3", "name": "Alice", "email": "alice@example.com"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 201

    data = resp.get_json()
    assert data["message"] == "User created"
    assert data["user"]["user_id"] == "3"

    assert "3" in fake_db

def test_create_user_missing_fields(client):
    resp = client.post("/users", json={"user_id": "4", "name": "Bob"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Missing required fields" in data.get("message", "")

def test_create_existing_user(client):
    existing_user = {"user_id": "1", "name": "Duplicate", "email": "dup@dup.com"}
    resp = client.post("/users", json=existing_user)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "User already exists" in data.get("message", "")

# PUT (Update)
def test_update_user_success(client):
    updated_data = {"name": "Johnny", "email": "johnny@newmail.com"}
    resp = client.put("/users/1", json=updated_data)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["message"] == "User updated"
    assert data["user"]["name"] == "Johnny"
    assert fake_db["1"]["email"] == "johnny@newmail.com"

def test_update_nonexistent_user(client):
    updated_data = {"name": "Ghost", "email": "ghost@no.com"}
    resp = client.put("/users/999", json=updated_data)
    assert resp.status_code == 404
    data = resp.get_json()
    assert "User not found" in data.get("message", "")

def test_update_user_without_json(client):
    resp = client.put("/users/1")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Missing JSON data" in data.get("message", "")

# DELETE
def test_delete_user_success(client):
    resp = client.delete("/users/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "User 1 deleted" in data["message"]
    assert "1" not in fake_db

def test_delete_nonexistent_user(client):
    resp = client.delete("/users/999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert "User not found" in data.get("message", "")

# INTEGRATION FLOW (end-to-end)
def test_full_crud_flow(client):
    # CREATE
    user_data = {"user_id": "10", "name": "Flow Test", "email": "flow@test.com"}
    resp_create = client.post("/users", json=user_data)
    assert resp_create.status_code == 201

    # READ
    resp_get = client.get("/users/10")
    assert resp_get.status_code == 200
    assert resp_get.get_json()["name"] == "Flow Test"

    # UPDATE
    resp_put = client.put("/users/10", json={"name": "Flow Updated"})
    assert resp_put.status_code == 200
    assert fake_db["10"]["name"] == "Flow Updated"

    # DELETE
    resp_del = client.delete("/users/10")
    assert resp_del.status_code == 200

    # CONFIRM DELETE
    resp_get2 = client.get("/users/10")
    assert resp_get2.status_code == 404