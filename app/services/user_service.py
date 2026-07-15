from fastapi import HTTPException, status
from app.schemas.users import UserCreate, UserUpdate
from typing import Dict, List, Any

users_mock: List[Dict[str, Any]] = [
    {"id": 1, "username": "nguyenvana", "email": "ana@gmail.com", "role": "admin", "is_active": True},
    {"id": 2, "username": "lethib", "email": "bthile@gmail.com", "role": "reader", "is_active": False}
]

class UserService:
    def get_all_users(self)-> List[Dict[str, Any]]:
        return users_mock
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        for user in users_mock:
            if user["id"] == user_id:
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        for user in users_mock:
            if user["username"].lower() == user_data.username.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This username is already taken"
                )
            if user["email"].lower() == user_data.email.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email is already registered"
                )
        new_id = users_mock[-1]["id"] + 1 if users_mock else 1
        new_user = {
            "id": new_id,
            "username": user_data.username,
            "email": user_data.email,
            "role": user_data.role,
            "is_active": user_data.is_active
        }
        users_mock.append(new_user)
        return new_user
    def update_user(self, user_id: int, user_data: UserUpdate) -> Dict[str, Any]:
        for user in users_mock:
            if user["id"] == user_id:
                # Trích xuất các trường thực sự được truyền lên
                update_data = user_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    user[key] = value
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        for index, user in enumerate(users_mock):
            if user["id"] == user_id:
                return users_mock.pop(index)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

user_service = UserService()