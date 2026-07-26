from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id:int
    # FIX: Cấu hình from_attributes=True để Pydantic v2 serialize được đối tượng SQLAlchemy ORM Model
    model_config = ConfigDict(from_attributes=True)