from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.authors import AuthorResponse
from app.schemas.categories import CategoryResponse

class BookBase(BaseModel):
    title: str
    author_id: int
    category_id: int
    published_year: int
    quantity: int = 1

class BookCreate(BookBase):
    available_quantity: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    published_year: Optional[int] = None
    quantity: Optional[int] = None
    available_quantity: Optional[int] = None

class BookResponse(BookBase):
    id: int
    available_quantity: int
    model_config = ConfigDict(from_attributes=True)

class BookDetailResponse(BookResponse):
    author: Optional[AuthorResponse] = None
    category: Optional[CategoryResponse] = None
