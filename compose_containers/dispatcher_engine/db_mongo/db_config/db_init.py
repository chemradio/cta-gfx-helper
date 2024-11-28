import os

from pymongo import MongoClient

# MONGODB_CONNECTION_STRING = (
#     f"mongodb://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@db:27017/"
# )

MONGODB_CONNECTION_STRING = f"mongodb://db:27017/"

client = MongoClient(MONGODB_CONNECTION_STRING)

# create objects / reinitialize tables and
db = client["cta-gfx-helper"]
Users = db.get_collection("users")
Orders = db.get_collection("orders")
