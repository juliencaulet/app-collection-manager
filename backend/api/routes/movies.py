from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.movie import Movie
from services.movie_service import MovieService
from core.security import get_current_user

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=Movie)
async def create_movie(movie: Movie, service: MovieService = Depends(), current_user = Depends(get_current_user)):
    """Create a new movie."""
    return await service.create_movie(movie)

@router.get("/", response_model=List[Movie])
async def get_all_movies(service: MovieService = Depends(), current_user = Depends(get_current_user)):
    """Get all movies."""
    return await service.get_all_movies()

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: str, service: MovieService = Depends(), current_user = Depends(get_current_user)):
    """Get a movie by ID."""
    return await service.get_movie(movie_id)

@router.put("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: str, movie: Movie, service: MovieService = Depends(), current_user = Depends(get_current_user)):
    """Update a movie."""
    return await service.update_movie(movie_id, movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str, service: MovieService = Depends(), current_user = Depends(get_current_user)):
    """Delete a movie."""
    return await service.delete_movie(movie_id)

@router.get("/search/", response_model=List[Movie])
async def search_movies(
    query: str = Query(..., description="Search query for title, director, or genre"),
    service: MovieService = Depends(),
    current_user = Depends(get_current_user)
):
    """Search movies by title, director, or genre."""
    return await service.search_movies(query)

@router.get("/collection/{collection_id}", response_model=List[Movie])
async def get_movies_by_collection(
    collection_id: str,
    service: MovieService = Depends(),
    current_user = Depends(get_current_user)
):
    """Get all movies in a collection."""
    return await service.get_movies_by_collection(collection_id)

@router.patch("/{movie_id}/status")
async def update_movie_status(
    movie_id: str,
    status: str = Query(..., description="New status (unwatched, watching, watched)"),
    service: MovieService = Depends(),
    current_user = Depends(get_current_user)
):
    """Update a movie's status."""
    return await service.update_movie_status(movie_id, status)

@router.patch("/{movie_id}/rating")
async def update_movie_rating(
    movie_id: str,
    rating: int = Query(..., ge=1, le=5, description="Rating from 1 to 5"),
    service: MovieService = Depends(),
    current_user = Depends(get_current_user)
):
    """Update a movie's rating."""
    return await service.update_movie_rating(movie_id, rating)
