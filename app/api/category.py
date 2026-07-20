from fastapi import APIRouter, HTTPException, Depends
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import Category, get_category_service
from app.models.category import Category
from typing import List, Dict, Any

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
FAKE_CATEGORY=[
        {"id":1,"name":"Programming", "description":"Books about software development"},
        {"id":2, "name":"Fiction","description":"Literature and novels"}
    ]
@router.get("/", response_model=List[CategoryResponse])
def get_categories(category_service: Category=Depends(get_category_service)):
    return category_service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, category_service: Category=Depends(get_category_service)):
    return category_service.get_category_by_id(category_id)

@router.post("/", response_model=CategoryResponse)
def create_categories(category_data:CategoryCreate, category_service:Category=Depends(get_category_service)):
    return category_service.create_category(category_data)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id:int, category_data:CategoryUpdate, category_service: Category=Depends(get_category_service)):
    return category_service.update_category(category_id, category_data)    

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(category_id:int, category_service: Category=Depends(get_category_service)):
    return category_service.delete_category(category_id)