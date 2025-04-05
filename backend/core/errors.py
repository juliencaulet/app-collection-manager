from fastapi import HTTPException, status

class CollectionManagerError(HTTPException):
    """Base exception for Collection Manager errors"""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ItemNotFoundError(CollectionManagerError):
    """Raised when a requested item is not found"""
    def __init__(self, item_type: str, item_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_type} with id {item_id} not found"
        )

class DatabaseError(CollectionManagerError):
    """Raised when there's an error with database operations"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class ValidationError(CollectionManagerError):
    """Raised when there's a validation error"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {detail}"
        ) 