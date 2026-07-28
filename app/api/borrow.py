from fastapi import APIRouter, Depends, status
from typing import List

from app.schemas.borrows import BorrowCreate, BorrowResponse
from app.services.borrow_service import BorrowService, get_borrow_service
from app.core.security import get_current_user, require_roles
from app.models.user import User

router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)

@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def create_borrow(
    borrow_data: BorrowCreate,
    service: BorrowService = Depends(get_borrow_service),
    current_user: User = Depends(get_current_user)
):
    return service.create_borrow(borrow_data)

@router.get("/", response_model=List[BorrowResponse], dependencies=[Depends(require_roles("admin", "librarian"))])
def get_borrows(
    service: BorrowService = Depends(get_borrow_service)
):
    return service.get_all_borrows()

@router.get("/overdue", response_model=List[BorrowResponse], dependencies=[Depends(require_roles("admin", "librarian"))])
def get_overdue_borrows(
    service: BorrowService = Depends(get_borrow_service)
):
    return service.get_overdue_borrows()

@router.get("/{borrow_id}", response_model=BorrowResponse)
def get_borrow_by_id(
    borrow_id: int,
    service: BorrowService = Depends(get_borrow_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_borrow_by_id(borrow_id)

@router.put("/{borrow_id}/return", response_model=BorrowResponse)
def return_book(
    borrow_id: int,
    service: BorrowService = Depends(get_borrow_service),
    current_user: User = Depends(get_current_user)
):
    return service.return_book(borrow_id)