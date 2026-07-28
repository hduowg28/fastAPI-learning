from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.books import BookCreate, BookUpdate, BookResponse, BookDetailResponse
from app.services.book_service import BookService, get_book_service
from app.core.security import require_roles

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/", response_model=List[BookDetailResponse])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    service: BookService = Depends(get_book_service)
):
    return service.get_all_books(
        skip=skip,
        limit=limit,
        title=title,
        author_id=author_id,
        category_id=category_id
    )

@router.get("/{book_id}", response_model=BookDetailResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.get_book_by_id(book_id)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin", "librarian"))])
def create_book(book_data: BookCreate, service: BookService = Depends(get_book_service)):
    return service.create_book(book_data)

@router.put("/{book_id}", response_model=BookResponse, dependencies=[Depends(require_roles("admin", "librarian"))])
def update_book(book_id: int, book_data: BookUpdate, service: BookService = Depends(get_book_service)):
    return service.update_book(book_id, book_data)

@router.delete("/{book_id}", response_model=BookResponse, dependencies=[Depends(require_roles("admin", "librarian"))])
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    return service.delete_book(book_id)