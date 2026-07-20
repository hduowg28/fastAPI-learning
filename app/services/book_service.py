from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.books import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository
from app.models.book import Book
from typing import List, Dict, Any
from app.core.database import get_db


class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BookRepository(db)
    def get_all_books(self):
        return self.repo.get_all()
    
    def get_book_by_id(self, book_id:int):
        book = self.repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return book
    
    async def create_book(self, book_data:BookCreate):
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
        return await self.repo.create(book_data)

    def update_book(self, book_id:int ,book_data:BookUpdate):
        db_book = self.repo.get_by_id(book_id)
        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="This book not found"
            )
        
        update_data = book_data.model_dump(exclude_unset=True)
        return self.repo.update(db_book, update_data)
    

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
