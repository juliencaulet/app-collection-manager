from typing import List, Optional
from fastapi import HTTPException
from models.book_series import BookSeries
from core.database import get_database
from datetime import datetime

class BookSeriesService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[BookSeries.Config.collection_name]

    async def create_series(self, series: BookSeries) -> BookSeries:
        """Create a new book series."""
        try:
            result = await self.collection.insert_one(series.dict())
            series.id = str(result.inserted_id)
            return series
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_series(self, series_id: str) -> Optional[BookSeries]:
        """Get a book series by ID."""
        series = await self.collection.find_one({"_id": series_id})
        if not series:
            raise HTTPException(status_code=404, detail="Book series not found")
        return BookSeries(**series)

    async def get_all_series(self) -> List[BookSeries]:
        """Get all book series."""
        cursor = self.collection.find()
        series = await cursor.to_list(length=None)
        return [BookSeries(**s) for s in series]

    async def update_series(self, series_id: str, series: BookSeries) -> BookSeries:
        """Update a book series."""
        series.updated_at = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": series_id},
            {"$set": series.dict(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Book series not found")
        return series

    async def delete_series(self, series_id: str) -> bool:
        """Delete a book series."""
        result = await self.collection.delete_one({"_id": series_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book series not found")
        return True

    async def search_series(self, query: str) -> List[BookSeries]:
        """Search book series by name or author."""
        cursor = self.collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}}
            ]
        })
        series = await cursor.to_list(length=None)
        return [BookSeries(**s) for s in series]

    async def add_book_to_series(self, series_id: str, book_id: str) -> BookSeries:
        """Add a book to a series."""
        series = await self.get_series(series_id)
        if book_id not in series.book_ids:
            series.book_ids.append(book_id)
            return await self.update_series(series_id, series)
        return series

    async def remove_book_from_series(self, series_id: str, book_id: str) -> BookSeries:
        """Remove a book from a series."""
        series = await self.get_series(series_id)
        if book_id in series.book_ids:
            series.book_ids.remove(book_id)
            return await self.update_series(series_id, series)
        return series

    async def update_series_status(self, series_id: str, status: str) -> BookSeries:
        """Update a book series's status."""
        series = await self.get_series(series_id)
        series.status = status
        series.updated_at = datetime.utcnow()
        return await self.update_series(series_id, series)
