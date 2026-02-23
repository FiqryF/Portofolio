from fastapi import APIRouter, HTTPException
from database import projects_collection
from models import ProjectSchema
from bson import ObjectId

router = APIRouter()

def serialize_doc(doc):
    return {**doc, "_id": str(doc["_id"])}

@router.get("/")
def get_projects():
    projects = list(projects_collection.find())
    return [serialize_doc(p) for p in projects]

@router.get("/{id}")
def get_project(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    project = projects_collection.find_one({"_id": ObjectId(id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialize_doc(project)

@router.post("/")
def create_project(project: ProjectSchema):
    new_project = project.dict()
    result = projects_collection.insert_one(new_project)
    return {"message": "Project created successfully", "id": str(result.inserted_id)}

@router.put("/{id}")
def update_project(id: str, project: ProjectSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = projects_collection.update_one({"_id": ObjectId(id)}, {"$set": project.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated successfully"}

@router.delete("/{id}")
def delete_project(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = projects_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
