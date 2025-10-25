from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake DB
fake_db = {}

# GET single user
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = fake_db.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# POST (create) user
@app.route("/users/<user_id>", methods=["POST"])
def create_user(user_id):
    if user_id in fake_db:
        return jsonify({"error": "User already exists"}), 400
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    fake_db[user_id] = {"user_id": user_id, "name": data["name"], "email": data["email"]}
    return jsonify(fake_db[user_id]), 201

# PUT (update) user
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in fake_db:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    fake_db[user_id].update(data)
    return jsonify(fake_db[user_id]), 200

# DELETE user
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in fake_db:
        return jsonify({"error": "User not found"}), 404
    del fake_db[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
