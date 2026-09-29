from pymongo import MongoClient
from core.config import settings

client = MongoClient(settings.MONGODB_URI)

db = client["welfare_ai"]