from pydantic import BaseModel 
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