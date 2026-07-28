from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.books import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.category_repository import CategoryRepository
from app.models.book import Book
from typing import List, Dict, Any
from app.core.database import get_db


class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)
        self.category_repo = CategoryRepository(db)

    def get_all_books(
        self,
        skip: int = 0,
        limit: int = 10,
        title: str = None,
        author_id: int = None,
        category_id: int = None
    ):
        return self.repo.get_all(
            skip=skip,
            limit=limit,
            title=title,
            author_id=author_id,
            category_id=category_id
        )

    
    def get_book_by_id(self, book_id:int):
        book = self.repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return book
    
    def create_book(self, book_data:BookCreate):
        # FIX: Kiểm tra xem Author và Category có tồn tại trong CSDL trước khi tạo sách để tránh lỗi ForeignKeyConstraint
        if not self.author_repo.get_by_id(book_data.author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with id {book_data.author_id} not found"
            )
        if not self.category_repo.get_by_id(book_data.category_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {book_data.category_id} not found"
            )

        existing_book = self.repo.check_duplicate(
            title=book_data.title,
            author_id=book_data.author_id,
            published_year=book_data.published_year
        )
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="This book already exists"
            )
        return self.repo.create(book_data)

    def update_book(self, book_id:int ,book_data:BookUpdate):
        db_book = self.repo.get_by_id(book_id)
        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="This book not found"
            )
        
        # FIX: Trước đây gọi model_dump() tạo ra dict rồi truyền vào repo.update, gây lỗi AttributeError: 'dict' object has no attribute 'model_dump' ở Repository.
        # Sửa lại: Truyền trực tiếp đối tượng Pydantic 'book_data' vào repo.update.
        return self.repo.update(db_book, book_data)
    

    def delete_book(self, book_id:int) -> Dict[str, Any]:
        book = self.repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This book not found"
            )
        return self.repo.delete(book)

def get_book_service(db: Session = Depends(get_db))-> BookService:
    return BookService(db)

