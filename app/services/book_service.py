from fastapi import HTTPException, status
from app.schemas.books import BookCreate, BookUpdate
from typing import List, Dict, Any

db_mock: List[Dict[str, Any]] = [
    {
        "id": 1, 
        "title": "Clean Code", 
        "author_id": 1,       
        "category_id": 2,      
        "published_year": 2008
    },
    {
        "id": 2, 
        "title": "Python Crash Course", 
        "author_id": 2, 
        "category_id": 1, 
        "published_year": 2015
    }
    ]

class BookService:
    def get_all_books(self) -> List[Dict[str, Any]]:
        return db_mock
    
    def get_book_by_id(self, book_id:int)->Dict[str, Any]:
        for book in db_mock:
            if book["id"]==book_id:
                return book
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    def create_book(self, book_data:BookCreate):
        for book in db_mock:
            if (book["title"]==book_data.title.lower() and 
                book["author_id"]==book_data.author_id and 
                book["published_year"]==book_data.published_year
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="this book already exists"
                )
        new_id =db_mock[-1]["id"]+1 if db_mock else 1
        new_book = {
            "id":new_id,
            "title":book_data.title,
            "author_id":book_data.author_id,
            "category_id":book_data.category_id,
            "published_year":book_data.published_year                   
        }
        db_mock.append(new_book)
        return new_book
    def update_book(self, book_id:int ,book_data:BookUpdate) -> Dict[str, Any]:
        for book in db_mock:
            if book["id"]==book_id:
                update_data=book_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    book[key]=value
                return book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this book not found")
    def delete_book(self, book_id:int) -> Dict[str, Any]:
        for index,book in enumerate(db_mock):
            if book["id"]==book_id:
                return db_mock.pop(index)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this book not found")
book_service = BookService()