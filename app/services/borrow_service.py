from fastapi import HTTPException, status
from typing import Dict, Any, List
from datetime import date
from schemas.borrows import BorrowCreate, BorrowUpdate 

users_mock = [
    {"id": 1, "username": "nguyenvana", "is_active": True},
    {"id": 2, "username": "lethib", "is_active": False} 
]


books_mock = [
    {"id": 1, "title": "Clean Code", "author_id": 1, "category_id": 2, "published_year": 2008},
    {"id": 2, "title": "Python Crash Course", "author_id": 2, "category_id": 1, "published_year": 2015}
]


borrows_mock: List[Dict[str, Any]] = [
    {
        "id": 1,
        "user_id": 1,
        "book_id": 1,
        "borrow_date": date(2026, 7, 1),
        "return_date": date(2026, 7, 15),
        "status": "borrowed" # Đang mượn
    }
]
class BorrowService: 
    def get_all_borrows(self) -> List[Dict[str, Any]]:
        return borrows_mock
    
    def create_borrow(self, borrow_data:BorrowCreate) -> Dict[str, Any]:
        user_valid=None 
        for u in users_mock:
            if u["id"]==borrow_data.user_id:
                user_valid=u
                break
        if not user_valid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        if not user_valid["is_active"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is not activated")
        
        book_exist=None
        for b in books_mock:
            if b["id"]==borrow_data.book_id:
                book_exist=b
                break
        if not book_exist: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="book not exist")
        for borrow in borrows_mock:
            if (borrow["user_id"] == borrow_data.user_id and 
                borrow["book_id"] == borrow_data.book_id and 
                borrow["status"] == "borrowed"):
                raise HTTPException(
                    status_code=400, 
                    detail="User is already borrowing this book and hasn't returned it yet"
                )
        new_id = borrows_mock[-1]["id"]+1 if borrows_mock else 1
        new_borrow={
            "id": new_id, 
            "user_id":borrow_data.user_id,
            "book_id":borrow_data.book_id, 
            "borrow_date":borrow_data.borrow_date,
            "return_date":borrow_data.return_date,
            "status":borrow_data.status
        }
        borrows_mock.append(new_borrow)
        return new_borrow
    
    def return_book(self, borrow_id:int) -> Dict[str, Any]:
        for borrow in borrows_mock:
            if borrow["id"]==borrow_id:
                if borrow["status"]=="returned":
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book was already returned") 
                borrow["status"]="returned"
                return borrow
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book haven't borrowed yet")
    
    def update_borrow(self, borrow_id: int, borrow_data: BorrowUpdate) -> Dict[str, Any]:
        for borrow in borrows_mock:
            if borrow["id"] == borrow_id:
                update_data = borrow_data.model_dump(exclude_unset=True)
                
                for key, value in update_data.items():
                    borrow[key] = value
                return borrow
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Borrow record not found"
        )
borrow_service=BorrowService()