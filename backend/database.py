from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["portfolio"]

users_collection = db["users"]
