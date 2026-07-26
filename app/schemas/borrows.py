from pydantic import BaseModel, ConfigDict 
from typing import Optional 
from datetime import date

class BorrowBase(BaseModel):
    user_id:int
    book_id:int
    borrow_date: date
    return_date:date
    status:str

class BorrowCreate(BorrowBase):
    pass

class BorrowUpdate(BaseModel):
    user_id:Optional[int] = None
    book_id:Optional[int] = None
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None
    status: Optional[str] = None

class BorrowResponse(BorrowBase):
    id:int
    # FIX: Cấu hình from_attributes=True để Pydantic v2 serialize được đối tượng SQLAlchemy ORM Model
    model_config = ConfigDict(from_attributes=True)