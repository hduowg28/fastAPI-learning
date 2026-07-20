from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.categories import CategoryCreate, CategoryUpdate
from typing import List, Optional

class CategoryRepository:
    def __init__(self, db: Session) :
        self.db=db

    def get_all(self)-> List[Category]:
        return self.db.query(Category).all()
    
    def get_by_id(self, category_id:int) -> Category:
        return self.db.query(Category).filter(Category.id==category_id).first()
    def get_by_name(self, name: str) -> Category | None:
        return (
            self.db.query(Category)
            .filter(Category.name.ilike(name))
            .first()
        )

    def create(self, category_data:CategoryCreate)-> Category:
        category_db=Category(name=category_data.name, description=category_data.description)
        self.db.add(category_db)
        self.db.commit()
        self.db.refresh(category_db)
        return category_db
    
    def update(self, category_db:Category, category_data:CategoryUpdate) -> Category:
        for key, value in category_data.model_dump(exclude_unset=True).items():
            setattr(category_db, key, value)
        self.db.commit()
        self.db.refresh(category_db)
        return category_db
    def delete(self, category_db: Category) -> Category:
        self.db.delete(category_db)
        self.db.commit()
        return category_db