from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.books import BookCreate, BookUpdate
from typing import List, Optional

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None
    ) -> List[Book]:
        query = self.db.query(Book)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author_id:
            query = query.filter(Book.author_id == author_id)
        if category_id:
            query = query.filter(Book.category_id == category_id)
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def check_duplicate(self, title: str, author_id: int, published_year: int) -> Optional[Book]:
        return self.db.query(Book).filter(
            Book.title.ilike(title),
            Book.author_id == author_id,
            Book.published_year == published_year
        ).first()

    def create(self, book_data: BookCreate) -> Book:
        avail_qty = book_data.available_quantity if book_data.available_quantity is not None else book_data.quantity
        db_book = Book(
            title=book_data.title,
            author_id=book_data.author_id,
            category_id=book_data.category_id,
            published_year=book_data.published_year,
            quantity=book_data.quantity,
            available_quantity=avail_qty
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book


    def update(self, db_book: Book, update_data: BookUpdate ) -> Book:
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(db_book, key, value)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, db_book: Book) -> Book:
        self.db.delete(db_book)
        self.db.commit()
        return db_book