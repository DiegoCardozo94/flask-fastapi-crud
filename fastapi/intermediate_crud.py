from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

fake_db = {}

class Item(BaseModel):
    name: str
    description: str = ""

# CREATE
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, response: Response):
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item_id] = item.dict()
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Item created", "item": fake_db[item_id]}

# READ (single item)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": item}

# READ (list all items)
@app.get("/items")
async def list_items():
    return fake_db

# UPDATE (PUT)
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, response: Response):
    if item_id in fake_db:
        fake_db[item_id].update(item.dict())
        response.status_code = status.HTTP_200_OK
        return {"message": "Item updated", "item": fake_db[item_id]}
    else:
        fake_db[item_id] = item.dict()
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Item created", "item": fake_db[item_id]}

# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return {"message": f"Item {item_id} deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
