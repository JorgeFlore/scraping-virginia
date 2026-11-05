from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="PAC API", version="1.0.0")

# Modelos
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Base de datos simulada
items_db = []

@app.get("/")
def read_root():
    return {"message": "API PAC funcionando"}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item no encontrado"}

@app.post("/items", response_model=Item)
def create_item(item: Item):
    items_db.append(item.dict())
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            items_db[i] = item.dict()
            return item
    return {"error": "Item no encontrado"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            del items_db[i]
            return {"message": "Item eliminado"}
    return {"error": "Item no encontrado"}