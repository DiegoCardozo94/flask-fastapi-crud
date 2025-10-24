from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# ---------- TESTS ----------
# GET ----> curl -X GET http://localhost:5000/users
# GET ----> curl -X GET http://localhost:5000/users/1
# POST ----> curl -X POST -H "Content-Type: application/json" -d '{"user_id": "3", "name": "John Doe", "email": "j@j.com"}' http://localhost:5000/users
# PUT ----> curl -X PUT -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "j@j.com"}' http://localhost:5000/users/1
# DELETE ----> curl -X DELETE http://localhost:5000/users/1

fake_db = {
    "1": {"user_id": "1", "name": "John Doe", "email": "j@j.com"},
    "2": {"user_id": "2", "name": "Jane Smith", "email": "jane@x.com"}
}

# HELPER FUNCTIONS 
def validate_user_data(data, require_id=True):
    """Valida el JSON recibido para crear/actualizar usuarios."""
    if not data:
        abort(400, description="Missing JSON data")

    required_fields = ["name", "email"]
    if require_id:
        required_fields.insert(0, "user_id")

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing field: {field}")

# Routes
@app.route("/")
def index():
    return jsonify({
        "message": "Flask Advanced CRUD API",
        "routes": {
            "GET /users": "Get all users",
            "GET /users/<user_id>": "Get a specific user",
            "POST /users": "Create a new user",
            "PUT /users/<user_id>": "Update a user",
            "DELETE /users/<user_id>": "Delete a user"
        }
    })

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(fake_db.values())), 200

# GET single user
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = fake_db.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user), 200

# CREATE user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    validate_user_data(data, require_id=True)

    user_id = data["user_id"]
    if user_id in fake_db:
        abort(400, description="User already exists")

    fake_db[user_id] = data
    return jsonify({"message": "User created", "user": data}), 201

# UPDATE user (PUT)
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    validate_user_data(data, require_id=False)

    if user_id not in fake_db:
        abort(404, description="User not found")

    fake_db[user_id].update(data)
    return jsonify({"message": "User updated", "user": fake_db[user_id]}), 200

# DELETE user
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in fake_db:
        abort(404, description="User not found")

    del fake_db[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 204

# CUSTOM ERROR HANDLERS
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": error.description}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
