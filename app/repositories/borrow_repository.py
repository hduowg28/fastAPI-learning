from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.borrow import Borrow
from app.schemas.borrows import BorrowCreate, BorrowUpdate


class BorrowRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Borrow]:
        return self.db.query(Borrow).all()

    def get_by_id(self, borrow_id: int) -> Optional[Borrow]:
        return (
            self.db.query(Borrow)
            .filter(Borrow.id == borrow_id)
            .first()
        )

    def create(self, borrow_data: BorrowCreate) -> Borrow:
        db_borrow = Borrow(
            user_id=borrow_data.user_id,
            book_id=borrow_data.book_id,
            borrow_date=borrow_data.borrow_date,
            return_date=borrow_data.return_date,
            status=borrow_data.status
        )

        self.db.add(db_borrow)
        self.db.commit()
        self.db.refresh(db_borrow)

        return db_borrow

    def update(self, db_borrow: Borrow, update_data: BorrowUpdate) -> Borrow:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(db_borrow, key, value)

        self.db.commit()
        self.db.refresh(db_borrow)

        return db_borrow

    def delete(self, db_borrow: Borrow) -> Borrow:
        self.db.delete(db_borrow)
        self.db.commit()

        return db_borrow
    def get_by_user_id(self, user_id: int) -> List[Borrow]:
        return self.db.query(Borrow).filter(Borrow.user_id == user_id).all()

    def get_by_book_id(self, book_id: int) -> List[Borrow]:
        return self.db.query(Borrow).filter(Borrow.book_id == book_id).all()

    def get_active_borrow(self, user_id: int, book_id: int) -> Optional[Borrow]:
        return (
            self.db.query(Borrow)
            .filter(
                Borrow.user_id == user_id,
                Borrow.book_id == book_id,
                Borrow.status == "Borrowed"
            )
            .first()
        )