from pydantic import BaseModel
from typing import Optional, List

class LoginSchema(BaseModel):
    username: str
    password: str

class ProjectSchema(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    link: Optional[str] = None
    tags: List[str] = []

class HeroSchema(BaseModel):
    title: str
    subtitle: str
    description: str

class AboutSchema(BaseModel):
    type: str  # e.g., 'education', 'experience', 'organization', 'certification'
    year: str
    title: str
    subtitle: str
    description: str
    icon: Optional[str] = None

class SkillSchema(BaseModel):
    category: str # e.g., 'frontend', 'iot', 'tools'
    name: str
    icon: Optional[str] = None
