from typing import List, Optional
from fastapi import HTTPException
from models.book import Book
from utils.database import get_database
from datetime import datetime

class BookService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[Book.Config.collection_name]

    async def create_book(self, book: Book) -> Book:
        """Create a new book."""
        try:
            result = await self.collection.insert_one(book.dict())
            book.id = str(result.inserted_id)
            return book
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_book(self, book_id: str) -> Optional[Book]:
        """Get a book by ID."""
        book = await self.collection.find_one({"_id": book_id})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return Book(**book)

    async def get_all_books(self) -> List[Book]:
        """Get all books."""
        cursor = self.collection.find()
        books = await cursor.to_list(length=None)
        return [Book(**b) for b in books]

    async def update_book(self, book_id: str, book: Book) -> Book:
        """Update a book."""
        book.updated_at = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": book_id},
            {"$set": book.dict(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    async def delete_book(self, book_id: str) -> bool:
        """Delete a book."""
        result = await self.collection.delete_one({"_id": book_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return True

    async def search_books(self, query: str) -> List[Book]:
        """Search books by title, author, or genre."""
        cursor = self.collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"genre": {"$regex": query, "$options": "i"}}
            ]
        })
        books = await cursor.to_list(length=None)
        return [Book(**b) for b in books]

    async def get_books_by_series(self, series_id: str) -> List[Book]:
        """Get all books in a series."""
        cursor = self.collection.find({"series_id": series_id})
        books = await cursor.to_list(length=None)
        return [Book(**b) for b in books]

    async def update_book_status(self, book_id: str, status: str) -> Book:
        """Update a book's status."""
        book = await self.get_book(book_id)
        book.status = status
        return await self.update_book(book_id, book)

    async def update_book_rating(self, book_id: str, rating: int) -> Book:
        """Update a book's rating."""
        book = await self.get_book(book_id)
        book.rating = rating
        return await self.update_book(book_id, book)
