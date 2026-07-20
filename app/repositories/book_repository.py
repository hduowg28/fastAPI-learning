from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.books import BookCreate, BookUpdate
from typing import List, Optional

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Book]:
        return self.db.query(Book).all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def check_duplicate(self, title: str, author_id: int, published_year: int) -> Optional[Book]:
        return self.db.query(Book).filter(
            Book.title.ilike(title),
            Book.author_id == author_id,
            Book.published_year == published_year
        ).first()

    def create(self, book_data: BookCreate) -> Book:
        db_book = Book(
            title=book_data.title,
            author_id=book_data.author_id,
            category_id=book_data.category_id,
            published_year=book_data.published_year
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update(self, db_book: Book, update_data: BookUpdate ) -> Book:
        for key, value in update_data.items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, db_book: Book) -> Book:
        self.db.delete(db_book)
        self.db.commit()
        return db_book