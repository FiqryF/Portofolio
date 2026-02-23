from fastapi import APIRouter, HTTPException
from database import skills_collection
from models import SkillSchema
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

@router.get("/")
def get_skills(category: str = None):
    query = {}
    if category:
        query["category"] = category
    skills = list(skills_collection.find(query))
    return [serialize_doc(skill) for skill in skills]

@router.get("/{id}")
def get_skill(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    skill = skills_collection.find_one({"_id": ObjectId(id)})
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return serialize_doc(skill)

@router.post("/")
def create_skill(skill: SkillSchema):
    new_skill = skill.dict()
    result = skills_collection.insert_one(new_skill)
    return {"message": "Skill created successfully", "id": str(result.inserted_id)}

@router.put("/{id}")
def update_skill(id: str, skill: SkillSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = skills_collection.update_one({"_id": ObjectId(id)}, {"$set": skill.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill updated successfully"}

@router.delete("/{id}")
def delete_skill(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = skills_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted successfully"}
