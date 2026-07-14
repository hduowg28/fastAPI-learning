from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username:str
    email: EmailStr
    role:str
    is_active: bool

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username:Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active:Optional[bool] = None

class UserResponse(UserBase):
    id:int