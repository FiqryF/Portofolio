from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["portfolio"]

users_collection = db["users"]
projects_collection = db["projects"]
hero_collection = db["hero"]
about_collection = db["about"]
skills_collection = db["skills"]
