from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()
fake_db = {}

class Item(BaseModel):
    name: str
    description: str = ""

# CREATE
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    if item_id in fake_db:
        return {"message": f"Item {item_id} already exists", "item": fake_db[item_id]}
    fake_db[item_id] = item.dict()
    return {"message": f"Item {item_id} created", "item": fake_db[item_id]}

# READ
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = fake_db.get(item_id)
    return {"item_id": item_id, "item": item}

# UPDATE
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id in fake_db:
        fake_db[item_id].update(item.dict())
        return {"message": f"Item {item_id} updated", "item": fake_db[item_id]}
    else:
        fake_db[item_id] = item.dict()
        return {"message": f"Item {item_id} created", "item": fake_db[item_id]}

# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id in fake_db:
        del fake_db[item_id]
        return {"message": f"Item {item_id} deleted"}
    return {"message": f"Item {item_id} does not exist"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
