from pydantic import BaseModel, ConfigDict
from typing import Optional 

class AuthorBase(BaseModel):
    name: str
    
class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str]=None

class AuthorResponse(AuthorBase):
    id: int
    # FIX: Cấu hình from_attributes=True để Pydantic v2 có thể serialize đối tượng SQLAlchemy ORM Model trả về từ FastAPI API
    model_config = ConfigDict(from_attributes=True)

