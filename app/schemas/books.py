from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookBase(BaseModel):
    title:str
    author_id:int
    category_id:int
    published_year:int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    published_year: Optional[int]=None

class BookResponse(BookBase):
    id:int
    # FIX: Cấu hình from_attributes=True để Pydantic v2 serialize được đối tượng SQLAlchemy ORM Model
    model_config = ConfigDict(from_attributes=True)