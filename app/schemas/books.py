from pydantic import BaseModel
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