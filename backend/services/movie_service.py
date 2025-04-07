from typing import List, Optional
from fastapi import HTTPException
from models.movie import Movie
from utils.database import get_database
from datetime import datetime

class MovieService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[Movie.Config.collection_name]

    async def create_movie(self, movie: Movie) -> Movie:
        """Create a new movie."""
        try:
            result = await self.collection.insert_one(movie.dict())
            movie.id = str(result.inserted_id)
            return movie
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_movie(self, movie_id: str) -> Optional[Movie]:
        """Get a movie by ID."""
        movie = await self.collection.find_one({"_id": movie_id})
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return Movie(**movie)

    async def get_all_movies(self) -> List[Movie]:
        """Get all movies."""
        cursor = self.collection.find()
        movies = await cursor.to_list(length=None)
        return [Movie(**m) for m in movies]

    async def update_movie(self, movie_id: str, movie: Movie) -> Movie:
        """Update a movie."""
        movie.updated_at = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": movie_id},
            {"$set": movie.dict(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie

    async def delete_movie(self, movie_id: str) -> bool:
        """Delete a movie."""
        result = await self.collection.delete_one({"_id": movie_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Movie not found")
        return True

    async def search_movies(self, query: str) -> List[Movie]:
        """Search movies by title, director, or genre."""
        cursor = self.collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"director": {"$regex": query, "$options": "i"}},
                {"genre": {"$regex": query, "$options": "i"}}
            ]
        })
        movies = await cursor.to_list(length=None)
        return [Movie(**m) for m in movies]

    async def get_movies_by_collection(self, collection_id: str) -> List[Movie]:
        """Get all movies in a collection."""
        cursor = self.collection.find({"collection_id": collection_id})
        movies = await cursor.to_list(length=None)
        return [Movie(**m) for m in movies]

    async def update_movie_status(self, movie_id: str, status: str) -> Movie:
        """Update a movie's status."""
        movie = await self.get_movie(movie_id)
        movie.status = status
        return await self.update_movie(movie_id, movie)

    async def update_movie_rating(self, movie_id: str, rating: int) -> Movie:
        """Update a movie's rating."""
        movie = await self.get_movie(movie_id)
        movie.rating = rating
        return await self.update_movie(movie_id, movie)
