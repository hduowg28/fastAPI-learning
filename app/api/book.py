from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.books import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService, get_book_service
from typing import List
from app.models.book import Book


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/", response_model=List[BookResponse])
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_all_books()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.get_book_by_id(book_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book_data:BookCreate, service: BookService = Depends(get_book_service)):
    return service.create_book(book_data)

@router.put("/{book_id}")
def update_book(book_id:int, book_data:BookUpdate, service: BookService = Depends(get_book_service)):
    return service.update_book(book_id, book_data)

@router.delete("/{book_id}")
def delete_book(book_id:int, service: BookService = Depends(get_book_service)):
    return service.delete_book(book_id)