from pydantic import BaseModel, EmailStr, ConfigDict
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
    # FIX: Cấu hình from_attributes=True để Pydantic v2 serialize được đối tượng SQLAlchemy ORM Model
    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
