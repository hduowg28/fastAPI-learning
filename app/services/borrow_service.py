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

        if book.available_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is out of stock (no available copies)"
            )

        # FIX: Kiểm tra xem user có đang mượn cuốn sách này mà chưa trả hay không
        active_borrow = self.repo.get_active_borrow(borrow_data.user_id, borrow_data.book_id)
        if active_borrow:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has already borrowed this book and not returned it yet"
            )

        # FIX: Kiểm tra ngày trả phải lớn hơn hoặc bằng ngày mượn
        if borrow_data.return_date < borrow_data.borrow_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="return_date must be after or equal to borrow_date"
            )

        # Trừ số lượng khả dụng
        book.available_quantity -= 1
        self.book_repo.db.commit()

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

        # Cộng lại số lượng khả dụng cho sách
        book = self.book_repo.get_by_id(borrow.book_id)
        if book:
            book.available_quantity += 1

        borrow.status = "returned"
        self.repo.db.commit()

        return self.repo.update(borrow, BorrowUpdate(status="returned"))


    # FIX: Bổ sung hàm get_overdue_borrows phục vụ endpoint GET /borrows/overdue
    def get_overdue_borrows(self) -> List[Borrow]:
        return self.repo.get_overdue_borrows()

    def delete_borrow(self, borrow_id: int) -> Borrow:
        borrow = self.get_borrow_by_id(borrow_id)

        return self.repo.delete(borrow)



def get_borrow_service(
    db: Session = Depends(get_db)
) -> BorrowService:
    return BorrowService(db)