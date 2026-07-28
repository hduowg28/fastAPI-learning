from fastapi import APIRouter, Depends, status
from typing import List

from app.schemas.users import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService, get_user_service
from app.core.security import get_current_user, require_roles
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Lấy thông tin người dùng đang đăng nhập dựa trên JWT Bearer Token.
    """
    return current_user

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_roles("admin", "librarian"))])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles("admin", "librarian"))])
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(user_data)

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles("admin"))])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return service.update_user(user_id, user_data)

@router.delete("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles("admin"))])
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.delete_user(user_id)