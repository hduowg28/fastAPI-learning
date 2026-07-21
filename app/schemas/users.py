from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username:str
    email: EmailStr 
    role:str = "user"
    is_active: bool = True

class UserCreate(UserBase):
    password:str 


class UserUpdate(BaseModel):
    username:Optional[str] = None
    email: Optional[str] = None
    password:Optional[str] = None
    role: Optional[str] = None
    is_active:Optional[bool] = None

class UserResponse(UserBase):
    id:int
