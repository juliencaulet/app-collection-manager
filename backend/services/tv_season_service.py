from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from config.database import get_database
from models.tv_season import TVSeason, TVSeasonCreate, TVSeasonUpdate, TVSeasonInDB
from bson import ObjectId

class TVSeasonService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.acm_tv_seasons

    async def create_tv_season(self, tv_season: TVSeasonCreate) -> TVSeason:
        tv_season_dict = tv_season.dict()
        tv_season_dict["created_at"] = datetime.utcnow()
        tv_season_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(tv_season_dict)
        created_tv_season = await self.collection.find_one({"_id": result.inserted_id})
        return TVSeason(**self._convert_id(created_tv_season))

    async def get_tv_season(self, tv_season_id: str) -> Optional[TVSeason]:
        tv_season = await self.collection.find_one({"_id": ObjectId(tv_season_id)})
        return TVSeason(**self._convert_id(tv_season)) if tv_season else None

    async def get_tv_seasons_by_show(
        self,
        show_id: str,
        skip: int = 0,
        limit: int = 10
    ) -> List[TVSeason]:
        cursor = self.collection.find({"show_id": show_id}).skip(skip).limit(limit)
        tv_seasons = await cursor.to_list(length=limit)
        return [TVSeason(**self._convert_id(tv_season)) for tv_season in tv_seasons]

    async def update_tv_season(self, tv_season_id: str, tv_season: TVSeasonUpdate) -> Optional[TVSeason]:
        update_data = {k: v for k, v in tv_season.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.collection.update_one(
                {"_id": ObjectId(tv_season_id)},
                {"$set": update_data}
            )
        
        updated_tv_season = await self.collection.find_one({"_id": ObjectId(tv_season_id)})
        return TVSeason(**self._convert_id(updated_tv_season)) if updated_tv_season else None

    async def delete_tv_season(self, tv_season_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(tv_season_id)})
        return result.deleted_count > 0

    def _convert_id(self, document: dict) -> dict:
        if document:
            document["id"] = str(document.pop("_id"))
        return document

def get_tv_season_service() -> TVSeasonService:
    db = get_database()
    return TVSeasonService(db) 