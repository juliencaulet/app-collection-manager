from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.movie_collection import MovieCollection
from services.movie_collection_service import MovieCollectionService
from utils.security import get_current_user

router = APIRouter(prefix="/movie-collections", tags=["movie-collections"])

@router.post("/", response_model=MovieCollection)
async def create_collection(collection: MovieCollection, service: MovieCollectionService = Depends(), current_user = Depends(get_current_user)):
    """Create a new movie collection."""
    return await service.create_collection(collection)

@router.get("/", response_model=List[MovieCollection])
async def get_all_collections(service: MovieCollectionService = Depends(), current_user = Depends(get_current_user)):
    """Get all movie collections."""
    return await service.get_all_collections()

@router.get("/{collection_id}", response_model=MovieCollection)
async def get_collection(collection_id: str, service: MovieCollectionService = Depends(), current_user = Depends(get_current_user)):
    """Get a movie collection by ID."""
    return await service.get_collection(collection_id)

@router.put("/{collection_id}", response_model=MovieCollection)
async def update_collection(collection_id: str, collection: MovieCollection, service: MovieCollectionService = Depends(), current_user = Depends(get_current_user)):
    """Update a movie collection."""
    return await service.update_collection(collection_id, collection)

@router.delete("/{collection_id}")
async def delete_collection(collection_id: str, service: MovieCollectionService = Depends(), current_user = Depends(get_current_user)):
    """Delete a movie collection."""
    return await service.delete_collection(collection_id)

@router.post("/{collection_id}/movies/{movie_id}")
async def add_movie_to_collection(collection_id: str, movie_id: str, service: MovieCollectionService = Depends()):
    """Add a movie to a collection."""
    return await service.add_movie_to_collection(collection_id, movie_id)

@router.delete("/{collection_id}/movies/{movie_id}")
async def remove_movie_from_collection(collection_id: str, movie_id: str, service: MovieCollectionService = Depends()):
    """Remove a movie from a collection."""
    return await service.remove_movie_from_collection(collection_id, movie_id)

@router.get("/search/", response_model=List[MovieCollection])
async def search_collections(
    query: str = Query(..., description="Search query for collection name or director"),
    service: MovieCollectionService = Depends(),
    current_user = Depends(get_current_user)
):
    """Search movie collections by name or director."""
    return await service.search_collections(query)
