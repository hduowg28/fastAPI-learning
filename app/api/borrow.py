from fastapi import APIRouter
from app.services.borrow_service import borrow_service
from app.schemas.borrows import BorrowCreate,BorrowUpdate
from typing import Dict, Any, List

router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)

@router.post("/", response_model=Dict[str, Any])
def create_borrow(borrow_data: BorrowCreate):
    return borrow_service.create_borrow(borrow_data)

@router.get("/", response_model=List[Dict[str, Any]])
def get_borrows():
    return borrow_service.get_all_borrows()

@router.put("/{borrow_id}")
def return_book(borrow_id:int):
    return borrow_service.return_book(borrow_id)

@router.get("/overdue")
def get_overdue_borrows():
    return [
        {
            "id": 99, 
            "user_id": 3, 
            "book_id": 2, 
            "borrow_date": "2026-05-01", 
            "status": "overdue"
        }
    ]