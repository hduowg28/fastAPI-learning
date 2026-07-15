from fastapi import APIRouter, HTTPException
from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.services.category_service import category_service
from typing import List, Dict, Any
router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
FAKE_CATEGORY=[
        {"id":1,"name":"Programming", "description":"Books about software development"},
        {"id":2, "name":"Fiction","description":"Literature and novels"}
    ]
@router.get("/", response_model=List[Dict[str, Any]])
def get_categories():
    return category_service.get_all_categories()

@router.get("/{category_id}", response_model=Dict[str, Any])
def get_category(category_id: int):
    return category_service.get_category_by_id(category_id)

@router.post("/", response_model=Dict[str, Any])
def create_categories(category_data:CategoryCreate):
    return category_service.create_category(category_data)

@router.put("/{category_id}", response_model=Dict[str, Any])
def update_category(category_id:int, category_data:CategoryUpdate):
    return category_service.update_category(category_id, category_data)    

@router.delete("/{category_id}", response_model=Dict[str, Any])
def delete_category(category_id:int):
    return category_service.delete_category(category_id)