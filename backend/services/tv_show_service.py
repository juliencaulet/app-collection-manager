from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from config.database import get_database
from models.tv_show import TVShow, TVShowCreate, TVShowUpdate, TVShowInDB
from bson import ObjectId

class TVShowService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.acm_tv_shows

    async def create_tv_show(self, tv_show: TVShowCreate) -> TVShow:
        tv_show_dict = tv_show.dict()
        tv_show_dict["created_at"] = datetime.utcnow()
        tv_show_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(tv_show_dict)
        created_tv_show = await self.collection.find_one({"_id": result.inserted_id})
        return TVShow(**self._convert_id(created_tv_show))

    async def get_tv_show(self, tv_show_id: str) -> Optional[TVShow]:
        tv_show = await self.collection.find_one({"_id": ObjectId(tv_show_id)})
        return TVShow(**self._convert_id(tv_show)) if tv_show else None

    async def get_tv_shows(
        self,
        skip: int = 0,
        limit: int = 10,
        title: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[TVShow]:
        query = {}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if status:
            query["status"] = status

        cursor = self.collection.find(query).skip(skip).limit(limit)
        tv_shows = await cursor.to_list(length=limit)
        return [TVShow(**self._convert_id(tv_show)) for tv_show in tv_shows]

    async def update_tv_show(self, tv_show_id: str, tv_show: TVShowUpdate) -> Optional[TVShow]:
        update_data = {k: v for k, v in tv_show.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.collection.update_one(
                {"_id": ObjectId(tv_show_id)},
                {"$set": update_data}
            )
        
        updated_tv_show = await self.collection.find_one({"_id": ObjectId(tv_show_id)})
        return TVShow(**self._convert_id(updated_tv_show)) if updated_tv_show else None

    async def delete_tv_show(self, tv_show_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(tv_show_id)})
        return result.deleted_count > 0

    def _convert_id(self, document: dict) -> dict:
        if document:
            document["id"] = str(document.pop("_id"))
        return document

def get_tv_show_service() -> TVShowService:
    db = get_database()
    return TVShowService(db) 