from pydantic import BaseModel
from typing import Optional 

class AuthorBase(BaseModel):
    name: str
    
class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str]=None

class AuthorResponse(AuthorBase):
    id: int
