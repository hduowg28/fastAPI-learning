from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserUpdate
from app.utils.hash import hash_password 


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_all_users(self) -> List[User]:
        return self.repo.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        return user

    def create_user(self, user_data: UserCreate) -> User:
        # 1. Kiểm tra email đã tồn tại
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # 2. Kiểm tra username đã tồn tại
        if self.repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # 3. Băm mật khẩu từ request
        hashed_pwd = hash_password(user_data.password)

        # 4. Truyền hashed_password sang Repository
        return self.repo.create(user_data, hashed_password=hashed_pwd)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        if hasattr(user_data, "password") and user_data.password:
            user_data.password = hash_password(user_data.password)

        return self.repo.update(user, user_data)

    def delete_user(self, user_id: int) -> User:
        user = self.get_user_by_id(user_id)

        return self.repo.delete(user)


def get_user_service(
    db: Session = Depends(get_db)
) -> UserService:
    return UserService(db)