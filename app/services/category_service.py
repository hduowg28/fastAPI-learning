from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.core.database import get_db


class CategoryService:
    def __init__(self, db:Session):
        self.repo=CategoryRepository(db)

    def get_all_categories(self) -> List[Category]:
        return self.repo.get_all()

    def get_category_by_id(self, category_id: int) -> Category:
        category_db = self.repo.get_by_id(category_id)
        if not category_db:
            raise HTTPException(status_code = 404, detail="not found")
        return category_db

    def create_category(self, category_data: CategoryCreate) -> Category:
        category = self.repo.get_by_name(category_data.name)

        if category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This category name already exists"
            )

        return self.repo.create(category_data)

    def update_category(self, category_id: int, category_data: CategoryUpdate) -> Category:
        category_db=self.repo.get_by_id(category_id)
        if not category_db:
            raise HTTPException(status_code=404, detail="not found")
        return self.repo.update(category_db, category_data)

    def delete_category(self, category_id: int) -> Category:
        category_db=self.repo.get_by_id(category_id)
        if not category_db:
            raise HTTPException(status_code=404, detail="not found")
        return self.repo.delete(category_db) 


def get_category_service(db:Session = Depends(get_db))-> CategoryService:
    return CategoryService(db)