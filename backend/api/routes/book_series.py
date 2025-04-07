from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.book_series import BookSeries
from services.book_series_service import BookSeriesService
from utils.security import get_current_user

router = APIRouter(prefix="/book-series", tags=["book-series"])

@router.post("/", response_model=BookSeries)
async def create_series(series: BookSeries, service: BookSeriesService = Depends(), current_user = Depends(get_current_user)):
    """Create a new book series."""
    return await service.create_series(series)

@router.get("/", response_model=List[BookSeries])
async def get_all_series(service: BookSeriesService = Depends(), current_user = Depends(get_current_user)):
    """Get all book series."""
    return await service.get_all_series()

@router.get("/{series_id}", response_model=BookSeries)
async def get_series(series_id: str, service: BookSeriesService = Depends(), current_user = Depends(get_current_user)):
    """Get a book series by ID."""
    return await service.get_series(series_id)

@router.put("/{series_id}", response_model=BookSeries)
async def update_series(series_id: str, series: BookSeries, service: BookSeriesService = Depends(), current_user = Depends(get_current_user)):
    """Update a book series."""
    return await service.update_series(series_id, series)

@router.delete("/{series_id}")
async def delete_series(series_id: str, service: BookSeriesService = Depends(), current_user = Depends(get_current_user)):
    """Delete a book series."""
    return await service.delete_series(series_id)

@router.post("/{series_id}/books/{book_id}")
async def add_book_to_series(series_id: str, book_id: str, service: BookSeriesService = Depends()):
    """Add a book to a series."""
    return await service.add_book_to_series(series_id, book_id)

@router.delete("/{series_id}/books/{book_id}")
async def remove_book_from_series(series_id: str, book_id: str, service: BookSeriesService = Depends()):
    """Remove a book from a series."""
    return await service.remove_book_from_series(series_id, book_id)

@router.get("/search/", response_model=List[BookSeries])
async def search_series(
    query: str = Query(..., description="Search query for series name or author"),
    service: BookSeriesService = Depends(),
    current_user = Depends(get_current_user)
):
    """Search book series by name or author."""
    return await service.search_series(query)

@router.patch("/{series_id}/status", response_model=BookSeries)
async def update_series_status(
    series_id: str,
    status: str = Query(..., description="New status for the series"),
    service: BookSeriesService = Depends(),
    current_user = Depends(get_current_user)
):
    """Update a book series's status."""
    return await service.update_series_status(series_id, status)
