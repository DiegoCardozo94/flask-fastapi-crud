from flask import Flask, jsonify, request, abort

app = Flask(__name__)

fake_db = {
    "1": {"user_id": "1", "name": "John Doe", "email": "j@j.com"},
    "2": {"user_id": "2", "name": "Jane Smith", "email": "jane@x.com"}
}

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
    if not data or "user_id" not in data or "name" not in data or "email" not in data:
        abort(400, description="Missing required fields")
    user_id = data["user_id"]
    if user_id in fake_db:
        abort(400, description="User already exists")

    fake_db[user_id] = data
    return jsonify({"message": "User created", "user": data}), 201

# UPDATE user
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON data")
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
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
