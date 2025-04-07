from typing import List, Optional
from fastapi import HTTPException
from models.movie_collection import MovieCollection
from utils.database import get_database
from datetime import datetime

class MovieCollectionService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[MovieCollection.Config.collection_name]

    async def create_collection(self, collection: MovieCollection) -> MovieCollection:
        """Create a new movie collection."""
        try:
            result = await self.collection.insert_one(collection.dict())
            collection.id = str(result.inserted_id)
            return collection
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_collection(self, collection_id: str) -> Optional[MovieCollection]:
        """Get a movie collection by ID."""
        collection = await self.collection.find_one({"_id": collection_id})
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        return MovieCollection(**collection)

    async def get_all_collections(self) -> List[MovieCollection]:
        """Get all movie collections."""
        cursor = self.collection.find()
        collections = await cursor.to_list(length=None)
        return [MovieCollection(**c) for c in collections]

    async def update_collection(self, collection_id: str, collection: MovieCollection) -> MovieCollection:
        """Update a movie collection."""
        collection.updated_at = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": collection_id},
            {"$set": collection.dict(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Collection not found")
        return collection

    async def delete_collection(self, collection_id: str) -> bool:
        """Delete a movie collection."""
        result = await self.collection.delete_one({"_id": collection_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Collection not found")
        return True

    async def add_movie_to_collection(self, collection_id: str, movie_id: str) -> MovieCollection:
        """Add a movie to a collection."""
        collection = await self.get_collection(collection_id)
        if movie_id not in collection.movies:
            collection.movies.append(movie_id)
            collection.total_movies += 1
            await self.update_collection(collection_id, collection)
        return collection

    async def remove_movie_from_collection(self, collection_id: str, movie_id: str) -> MovieCollection:
        """Remove a movie from a collection."""
        collection = await self.get_collection(collection_id)
        if movie_id in collection.movies:
            collection.movies.remove(movie_id)
            collection.total_movies -= 1
            await self.update_collection(collection_id, collection)
        return collection
