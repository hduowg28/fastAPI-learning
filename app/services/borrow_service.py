from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.borrow import Borrow
from app.repositories.borrow_repository import BorrowRepository
from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository
from app.schemas.borrows import BorrowCreate, BorrowUpdate


class BorrowService:
    def __init__(self, db: Session):
        self.repo = BorrowRepository(db)
        self.user_repo = UserRepository(db)
        self.book_repo = BookRepository(db)

    def get_all_borrows(self) -> List[Borrow]:
        return self.repo.get_all()

    def get_borrow_by_id(self, borrow_id: int) -> Borrow:
        borrow = self.repo.get_by_id(borrow_id)

        if not borrow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Borrow record not found"
            )

        return borrow

    def create_borrow(self, borrow_data: BorrowCreate) -> Borrow:
        # Kiểm tra user
        user = self.user_repo.get_by_id(borrow_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not active"
            )

        # Kiểm tra book
        book = self.book_repo.get_by_id(borrow_data.book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # Có thể bổ sung kiểm tra mượn trùng ở đây nếu repository hỗ trợ

        return self.repo.create(borrow_data)

    def update_borrow(
        self,
        borrow_id: int,
        borrow_data: BorrowUpdate
    ) -> Borrow:

        borrow = self.get_borrow_by_id(borrow_id)

        return self.repo.update(borrow, borrow_data)

    def return_book(self, borrow_id: int) -> Borrow:
        borrow = self.get_borrow_by_id(borrow_id)

        if borrow.status == "returned":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book was already returned"
            )

        borrow.status = "returned"

        return self.repo.update(borrow, BorrowUpdate(status="returned"))

    def delete_borrow(self, borrow_id: int) -> Borrow:
        borrow = self.get_borrow_by_id(borrow_id)

        return self.repo.delete(borrow)


def get_borrow_service(
    db: Session = Depends(get_db)
) -> BorrowService:
    return BorrowService(db)