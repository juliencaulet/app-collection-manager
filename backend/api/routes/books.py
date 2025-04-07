from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.book import Book
from services.book_service import BookService
from utils.security import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
async def create_book(book: Book, service: BookService = Depends(), current_user = Depends(get_current_user)):
    """Create a new book."""
    return await service.create_book(book)

@router.get("/", response_model=List[Book])
async def get_all_books(service: BookService = Depends(), current_user = Depends(get_current_user)):
    """Get all books."""
    return await service.get_all_books()

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, service: BookService = Depends(), current_user = Depends(get_current_user)):
    """Get a book by ID."""
    return await service.get_book(book_id)

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book, service: BookService = Depends(), current_user = Depends(get_current_user)):
    """Update a book."""
    return await service.update_book(book_id, book)

@router.delete("/{book_id}")
async def delete_book(book_id: str, service: BookService = Depends(), current_user = Depends(get_current_user)):
    """Delete a book."""
    return await service.delete_book(book_id)

@router.get("/search/", response_model=List[Book])
async def search_books(
    query: str = Query(..., description="Search query for title, author, or genre"),
    service: BookService = Depends(),
    current_user = Depends(get_current_user)
):
    """Search books by title, author, or genre."""
    return await service.search_books(query)

@router.get("/series/{series_id}", response_model=List[Book])
async def get_books_by_series(
    series_id: str,
    service: BookService = Depends(),
    current_user = Depends(get_current_user)
):
    """Get all books in a series."""
    return await service.get_books_by_series(series_id)

@router.patch("/{book_id}/status")
async def update_book_status(
    book_id: str,
    status: str = Query(..., description="New status (unread, reading, read)"),
    service: BookService = Depends(),
    current_user = Depends(get_current_user)
):
    """Update a book's status."""
    return await service.update_book_status(book_id, status)

@router.patch("/{book_id}/rating")
async def update_book_rating(
    book_id: str,
    rating: int = Query(..., ge=1, le=5, description="Rating from 1 to 5"),
    service: BookService = Depends(),
    current_user = Depends(get_current_user)
):
    """Update a book's rating."""
    return await service.update_book_rating(book_id, rating)
