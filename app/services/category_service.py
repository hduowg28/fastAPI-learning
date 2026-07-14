from fastapi import HTTPException, status
from typing import List, Dict, Any
from app.schemas.categories import CategoryCreate, CategoryUpdate

categories_mock: List[Dict[str, Any]] = [
    {"id": 1, "name": "Lập trình", "description": "Sách hướng dẫn code và tư duy thuật toán"},
    {"id": 2, "name": "Khoa học học", "description": "Sách về thiên văn, vũ trụ và vật lý"}
]

class CategoryService:
    def get_all_categories(self) -> List[Dict[str, Any]]:
        return categories_mock

    def get_category_by_id(self, category_id: int) -> Dict[str, Any]:
        for cat in categories_mock:
            if cat["id"] == category_id:
                return cat
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )

    def create_category(self, category_data: CategoryCreate) -> Dict[str, Any]:
        for cat in categories_mock:
            if cat["name"].lower() == category_data.name.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This category name already exists"
                )
                
        new_id = categories_mock[-1]["id"] + 1 if categories_mock else 1
        new_cat = {
            "id": new_id,
            "name": category_data.name,
            "description": category_data.description
        }
        categories_mock.append(new_cat)
        return new_cat

    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Dict[str, Any]:
        for cat in categories_mock:
            if cat["id"] == category_id:
                update_data = category_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    cat[key] = value
                return cat
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )

    def delete_category(self, category_id: int) -> Dict[str, Any]:
        for index, cat in enumerate(categories_mock):
            if cat["id"] == category_id:
                return categories_mock.pop(index)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )

category_service = CategoryService()