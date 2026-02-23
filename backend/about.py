from fastapi import APIRouter, HTTPException
from database import about_collection
from models import AboutSchema
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

@router.get("/")
def get_about_items(type: str = None):
    query = {}
    if type:
        query["type"] = type
    items = list(about_collection.find(query).sort("year", -1))
    return [serialize_doc(item) for item in items]

@router.get("/{id}")
def get_about_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    item = about_collection.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize_doc(item)

@router.post("/")
def create_about_item(item: AboutSchema):
    new_item = item.dict()
    result = about_collection.insert_one(new_item)
    return {"message": "Item created successfully", "id": str(result.inserted_id)}

@router.put("/{id}")
def update_about_item(id: str, item: AboutSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = about_collection.update_one({"_id": ObjectId(id)}, {"$set": item.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated successfully"}

@router.delete("/{id}")
def delete_about_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = about_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
