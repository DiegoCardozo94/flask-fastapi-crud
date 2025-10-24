from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = {"user_id": user_id, "name": "John Doe", "email": "j@j.com"}
    return jsonify(user)

@app.route("/users/<user_id>", methods=["POST"])
def create_user(user_id):
    data = request.get_json()
    return jsonify({"user_id": user_id, "data": data}), 201

@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = {"user_id": user_id, "name": "John Doe", "email": "j@j.com"}
    return jsonify(user)

@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    return jsonify({"message": "User deleted"}), 204

if __name__ == "__main__":
    app.run(debug=True)
