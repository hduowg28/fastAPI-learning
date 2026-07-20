from fastapi import APIRouter, Depends, status
from typing import List

from app.schemas.borrows import BorrowCreate, BorrowResponse
from app.services.borrow_service import BorrowService, get_borrow_service

router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)

@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def create_borrow(
    borrow_data: BorrowCreate,
    service: BorrowService = Depends(get_borrow_service)
):
    return service.create_borrow(borrow_data)

@router.get("/", response_model=List[BorrowResponse])
def get_borrows(
    service: BorrowService = Depends(get_borrow_service)
):
    return service.get_all_borrows()

@router.put("/{borrow_id}", response_model=BorrowResponse)
def return_book(
    borrow_id: int,
    service: BorrowService = Depends(get_borrow_service)
):
    return service.return_book(borrow_id)

@router.get("/overdue", response_model=List[BorrowResponse])
def get_overdue_borrows(
    service: BorrowService = Depends(get_borrow_service)
):
    return service.get_overdue_borrows()