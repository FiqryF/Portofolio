from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from jose import jwt
from database import users_collection
from models import LoginSchema
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


# 🔐 REGISTER USER (auto hash password)
@router.post("/register")
def register(data: LoginSchema):
    existing_user = users_collection.find_one({"username": data.username})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(data.password)

    users_collection.insert_one({
        "username": data.username,
        "password": hashed_password
    })

    return {"message": "User created successfully"}


# 🔑 LOGIN USER
@router.post("/login")
def login(data: LoginSchema):
    user = users_collection.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = jwt.encode(
        {"id": str(user["_id"])},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}
