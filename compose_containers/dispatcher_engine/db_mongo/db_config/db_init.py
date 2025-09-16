import os
from pymongo import MongoClient


IS_DOCKER = os.getenv("IS_DOCKER", False)
MONGODB_CONNECTION_STRING = (
    f"mongodb://db:27017/" if IS_DOCKER else "mongodb://localhost:27017/"
)

client = MongoClient(MONGODB_CONNECTION_STRING)

db = client["cta-gfx-helper"]
Users = db.get_collection("users")
Orders = db.get_collection("orders")
Quotes = db.get_collection("quotes")
