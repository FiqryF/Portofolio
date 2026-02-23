from fastapi import APIRouter, HTTPException
from database import hero_collection
from models import HeroSchema
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

@router.get("/")
def get_hero():
    hero = hero_collection.find_one()
    if not hero:
        # Return default if empty
        return {"title": "Creating Digital Masterpieces.", "subtitle": "IoT & Frontend Developer", "description": "Welcome to my portfolio."}
    return serialize_doc(hero)

@router.post("/")
def update_hero(hero: HeroSchema):
    # Since hero is a singleton, we check if one exists
    existing = hero_collection.find_one()
    if existing:
        hero_collection.update_one({"_id": existing["_id"]}, {"$set": hero.dict()})
        return {"message": "Hero section updated successfully"}
    else:
        hero_collection.insert_one(hero.dict())
        return {"message": "Hero section created successfully"}
