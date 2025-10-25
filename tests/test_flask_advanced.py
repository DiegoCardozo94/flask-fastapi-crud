import pytest
from flask.testing import FlaskClient
from flask_cruds.advanced import app, fake_db

@pytest.fixture()
def client() -> FlaskClient:
    app.config["TESTING"] = True

    fake_db.clear()
    fake_db.update({
        "1": {"user_id": "1", "name": "John Doe", "email": "j@j.com"},
        "2": {"user_id": "2", "name": "Jane Smith", "email": "jane@x.com"},
    })

    with app.test_client() as client:
        yield client

# ROOT ROUTE
def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "Flask Advanced CRUD API" in data["message"]
    assert "GET /users" in data["routes"]

# GET ALL USERS
def test_get_all_users(client):
    resp = client.get("/users")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all("user_id" in u for u in data)

# GET SINGLE USER
def test_get_single_user_success(client):
    resp = client.get("/users/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["user_id"] == "1"
    assert data["name"] == "John Doe"

def test_get_single_user_not_found(client):
    resp = client.get("/users/999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "Not Found"
    assert "User not found" in data["message"]

# CREATE USER
def test_create_user_success(client):
    new_user = {"user_id": "3", "name": "Alice", "email": "alice@example.com"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "User created"
    assert data["user"]["user_id"] == "3"
    assert "3" in fake_db

def test_create_user_missing_field(client):
    incomplete_user = {"name": "Bob"}
    resp = client.post("/users", json=incomplete_user)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "Bad Request"
    assert "Missing field" in data["message"]

def test_create_user_duplicate(client):
    duplicate_user = {"user_id": "1", "name": "Dup", "email": "dup@dup.com"}
    resp = client.post("/users", json=duplicate_user)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["message"] == "User already exists"

def test_create_user_no_json(client):
    resp = client.post("/users", data="notjson")
    assert resp.status_code in (400, 415)
    data = resp.get_json()
    assert data["error"] == "Bad Request"

# UPDATE USER
def test_update_user_success(client):
    resp = client.put("/users/1", json={"name": "Updated Name", "email": "new@mail.com"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "User updated"
    assert data["user"]["name"] == "Updated Name"
    assert fake_db["1"]["email"] == "new@mail.com"

def test_update_user_not_found(client):
    resp = client.put("/users/999", json={"name": "Ghost", "email": "ghost@mail.com"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["message"] == "User not found"

def test_update_user_missing_field(client):
    resp = client.put("/users/1", json={"name": "No email"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Missing field" in data["message"]

def test_update_user_no_json(client):
    resp = client.put("/users/1")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Missing JSON data" in data["message"]

# DELETE USER
def test_delete_user_success(client):
    resp = client.delete("/users/1")
    assert resp.status_code == 204
    assert "1" not in fake_db

def test_delete_user_not_found(client):
    resp = client.delete("/users/999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["message"] == "User not found"

# INTEGRATION FLOW (END-TO-END)
def test_full_crud_flow(client):
    # CREATE
    new_user = {"user_id": "10", "name": "Flow User", "email": "flow@test.com"}
    resp_create = client.post("/users", json=new_user)
    assert resp_create.status_code == 201

    # READ
    resp_get = client.get("/users/10")
    assert resp_get.status_code == 200
    assert resp_get.get_json()["name"] == "Flow User"

    # UPDATE
    resp_put = client.put("/users/10", json={"name": "Updated Flow", "email": "upd@test.com"})
    assert resp_put.status_code == 200
    assert fake_db["10"]["name"] == "Updated Flow"

    # DELETE
    resp_del = client.delete("/users/10")
    assert resp_del.status_code == 204

    # CONFIRM DELETED
    resp_get2 = client.get("/users/10")
    assert resp_get2.status_code == 404