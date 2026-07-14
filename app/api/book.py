from fastapi import APIRouter, HTTPException, status
from app.schemas.books import BookCreate, BookUpdate
from app.services.book_service import book_service
from typing import List, Dict, Any

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/", response_model=List[Dict[str, Any]])
def get_books():
    return book_service.get_all_books()

@router.get("/{book_id}", response_model=Dict[str, Any])
def get_book(book_id: int):
    return book_service.get_book_by_id(book_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book_data:BookCreate):
    return book_service.create_book(book_data)

@router.put("/{book_id}")
def update_book(book_id:int, book_data:BookUpdate):
    return book_service.update_book(book_id, book_data)

@router.delete("/{book_id}")
def delete_book(book_id:int):
    return book_service.delete_book(book_id)