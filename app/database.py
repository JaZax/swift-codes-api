import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = MongoClient(mongo_uri)
db = client["swift_codes_db"]
