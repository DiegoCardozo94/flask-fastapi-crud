from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status, Response, Request

from pydantic import BaseModel
import uvicorn
import logging

app = FastAPI()

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crud_advanced")

fake_db = {}

class Item(BaseModel):
    name: str
    description: str = ""

class StandardResponse(BaseModel):
    status: str
    message: str
    data: dict | None = None

# CREATE
@app.post("/items/{item_id}", response_model=StandardResponse)
async def create_item(item_id: int, item: Item, response: Response):
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item_id] = item.dict()
    response.status_code = status.HTTP_201_CREATED
    logger.info(f"Item {item_id} created")
    return {"status": "success", "message": "Item created", "data": fake_db[item_id]}

# READ (single item)
@app.get("/items/{item_id}", response_model=StandardResponse)
async def read_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "success", "message": "Item retrieved", "data": item}

# READ (list all items)
@app.get("/items", response_model=StandardResponse)
async def list_items(name: str | None = None):
    items = fake_db
    if name:
        items = {k: v for k, v in fake_db.items() if name.lower() in v["name"].lower()}
    return {"status": "success", "message": "Items listed", "data": items}

# UPDATE (PUT)
@app.put("/items/{item_id}", response_model=StandardResponse)
async def update_item(item_id: int, item: Item, response: Response):
    if item_id in fake_db:
        fake_db[item_id].update(item.dict())
        response.status_code = status.HTTP_200_OK
        logger.info(f"Item {item_id} updated")
        return {"status": "success", "message": "Item updated", "data": fake_db[item_id]}
    else:
        fake_db[item_id] = item.dict()
        response.status_code = status.HTTP_201_CREATED
        logger.info(f"Item {item_id} created via PUT")
        return {"status": "success", "message": "Item created", "data": fake_db[item_id]}

# DELETE
@app.delete("/items/{item_id}", response_model=StandardResponse)
async def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    logger.info(f"Item {item_id} deleted")
    return {"status": "success", "message": f"Item {item_id} deleted", "data": None}

# HANDLERS
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail, "data": None}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal Server Error", "data": None}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
