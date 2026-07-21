from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.email.ilike(email))
            .first()
        )

    def get_by_username(self, username: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.username.ilike(username))
            .first()
        )

    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """
        Tạo user mới. 
        Mật khẩu đã được băm (hashed_password) từ Service layer sẽ truyền vào đây.
        """
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password, 
            role=user_data.role,
            is_active=user_data.is_active
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def update(self, db_user: User, update_data: UserUpdate) -> User:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def delete(self, db_user: User) -> User:
        self.db.delete(db_user)
        self.db.commit()

        return db_user
    
