from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "acm_db")

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

def get_database():
    """Get the database instance."""
    return db
