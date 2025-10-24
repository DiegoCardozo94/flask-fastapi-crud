# flask-fastapi-crud

CRUD examples in Python using Flask and FastAPI (basic, intermediate, advanced)

# FastAPI CRUD Practice

Practice with **FastAPI** to implement **Basic**, **Intermediate**, and **Advanced** CRUDs.  
This repository demonstrates the evolution of REST APIs in Python, from minimal examples to production-ready patterns.

---

## 🚀 CRUD Levels

We implemented three levels of CRUD complexity:

| Level       | Characteristics | Example / Concept |
|------------|----------------|-----------------|
| **Basic** | - Minimal CRUD<br>- Simple in-memory dictionary (`fake_db`) mapping `id` → `item`<br>- No validation<br>- Fixed status codes (200 or 201)<br>- No error handling | ```python\nfake_db = {}\n@app.post(\"/items/{id}\")\nasync def create_item(id: int):\n    fake_db[id] = {\"id\": id}\n    return {\"id\": id}\n``` |
| **Intermediate** | - Validation with **Pydantic** (`Item` model)<br>- Dynamic status codes (201 for creation, 200 for update)<br>- Error handling with `HTTPException`<br>- List all items endpoint<br>- Structured dictionary for items | ```python\nclass Item(BaseModel):\n    name: str\n    description: str = \"\"\n@app.get(\"/items/{id}\")\nasync def read_item(id: int):\n    item = fake_db.get(id)\n    if not item: raise HTTPException(404, \"Not found\")\n    return item\n``` |
| **Advanced** | - All features of Intermediate<br>- Standardized response format (`status`, `message`, `data`)<br>- Centralized custom error handlers<br>- Logging of CRUD operations<br>- Filters and search (e.g., `GET /items?name=...`)<br>- Ready for DB integration and authentication<br>- Modularized code using `Depends` | ```python\nclass StandardResponse(BaseModel):\n    status: str\n    message: str\n    data: dict | None = None\n@app.exception_handler(HTTPException)\nasync def http_exception_handler(req, exc):\n    return JSONResponse(...)\n``` |

---

## 📌 Endpoints Overview

### Basic CRUD
- `POST /items/{id}` → Create item with just `id`
- `GET /items/{id}` → Read item
- `PUT /items/{id}` → Update item (replace)
- `DELETE /items/{id}` → Delete item

### Intermediate CRUD
- `POST /items/{id}` → Create item with `name` and `description`
- `GET /items/{id}` → Read item by id
- `GET /items` → List all items
- `PUT /items/{id}` → Update or create item
- `DELETE /items/{id}` → Delete item

### Advanced CRUD
- `POST /items/{id}` → Create item with standardized response
- `GET /items/{id}` → Read single item with standardized response
- `GET /items?name=filter` → List all items or filter by name
- `PUT /items/{id}` → Update or create item with logging
- `DELETE /items/{id}` → Delete item with logging
- Centralized error handling for HTTP and general errors
- Response format consistent across all endpoints

---

## ⚡ Features Summary

- **Basic:** Learn endpoints, minimal FastAPI usage  
- **Intermediate:** Validation, dynamic status codes, proper error handling  
- **Advanced:** Production-ready patterns, logging, standardized responses, filters, and scalable code  

---

## 📝 Usage

1. Clone the repo:
```bash
git clone <repo-url>

```

2. Install dependencies
```
pip install fastapi uvicorn pydantic flask
```

3. Run FASTAPI examples
```
uvicorn main:app --reload
```

4. Explore API docs (for FastAPI) at:
```
http://127.0.0.1:8000/docs
```

# Python APIs - Flask CRUD Practice

Practice with **Flask** to implement **Basic**, **Intermediate**, and **Advanced** CRUD APIs.  
This repository demonstrates the evolution of REST APIs in Flask, from minimal examples to production-ready patterns.

---

## 🚀 CRUD Levels

We implemented three levels of CRUD complexity:

| Level       | Characteristics | Example / Concept |
|------------|----------------|-----------------|
| **Basic** | - Minimal CRUD<br>- Simple endpoints with static responses<br>- No validation or error handling<br>- No in-memory DB | ```python\n@app.route("/users/<user_id>", methods=["POST"])\ndef create_user(user_id):\n    data = request.get_json()\n    return jsonify({"user_id": user_id, "data": data}), 201\n``` |
| **Intermediate** | - In-memory dictionary (`fake_db`) to store users<br>- Validation of required fields<br>- Dynamic status codes (200/201)<br>- Error handling using `abort()`<br>- Full CRUD operations | ```python\nfake_db = {}\n@app.route("/users/<user_id>", methods=["GET"])\ndef get_user(user_id):\n    user = fake_db.get(user_id)\n    if not user: abort(404, "User not found")\n    return jsonify(user), 200\n``` |
| **Advanced** | - All features of Intermediate<br>- Standardized routes for listing all users<br>- Helper functions for validation<br>- Custom error handlers (400, 404, 500)<br>- Ready for more complex operations and scaling | ```python\ndef validate_user_data(data, require_id=True):\n    if not data: abort(400, "Missing JSON data")\n@app.errorhandler(404)\ndef not_found(error):\n    return jsonify({"error": "Not Found", "message": error.description}), 404\n``` |

---

## 📌 Endpoints Overview

### Basic CRUD (Flask)
- `POST /users/<user_id>` → Create a user
- `GET /users/<user_id>` → Read user
- `PUT /users/<user_id>` → Update user
- `DELETE /users/<user_id>` → Delete user

### Intermediate CRUD (Flask)
- `POST /users` → Create user with validation
- `GET /users/<user_id>` → Read single user
- `PUT /users/<user_id>` → Update user
- `DELETE /users/<user_id>` → Delete user
- Uses in-memory `fake_db` and proper error responses

### Advanced CRUD (Flask)
- `GET /users` → List all users
- `POST /users` → Create user with validation
- `GET /users/<user_id>` → Read single user
- `PUT /users/<user_id>` → Update user
- `DELETE /users/<user_id>` → Delete user
- Centralized custom error handlers (400, 404, 500)
- Helper function for validating user input
- Standardized JSON responses

---

## ⚡ Features Summary

- **Basic:** Minimal endpoints, no validation, static responses  
- **Intermediate:** In-memory DB, validation, error handling, dynamic status codes  
- **Advanced:** All CRUD operations, custom error handlers, validation helpers, list all users, scalable for future enhancements  

---

## 📝 Usage

1. Clone the repo:
```bash
git clone <repo-url>
```

2. Install dependencies
```
pip install flask
```
3. Run Flask examples
```
python basic.py      # Basic CRUD
python intermediate.py  # Intermediate CRUD
python advanced.py      # Advanced CRUD
```
4. Access endpoints
```
http://127.0.0.1:5000/users
```

5. Explore and test using curl or Postman.