import certifi
from pymongo import MongoClient
from core.config import settings

client = MongoClient(
    settings.MONGODB_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

db = client["welfare_ai"]
schemes_collection = db["schemes"]