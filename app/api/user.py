from fastapi import APIRouter, HTTPException
from typing import Any, List, Dict
from services.user_service import user_service
from schemas.users import UserCreate, UserUpdate

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)

@router.get("/", response_model=List[Dict[str, Any]])
def get_users():
    return user_service.get_all_users

@router.get("/{user_id}", response_model=Dict[str, Any])
def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

@router.post("/", response_model=Dict[str, Any])
def create_user(user_data:UserCreate):
    return user_service.create_user(user_data)

@router.put("/{user_id}", response_model=Dict[str, Any])
def update_user(user_id:int, update_data: UserUpdate):
    return user_service.update_user(user_id, update_data)

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return user_service.delete_user()
