from motor.motor_asyncio import AsyncIOMotorClient
from .environment import get_mongodb_url, get_mongodb_db_name

# Create MongoDB client
client = AsyncIOMotorClient(get_mongodb_url())

# Get database
def get_database():
    return client[get_mongodb_db_name()]
