from fastapi import APIRouter, HTTPException
from schemas.authors import AuthorCreate, AuthorUpdate
from services.author_service import author_service
from typing import Dict, Any, List

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)
FAKE_AUTHORS= [
        {"id":1,"name":"Harry Maguire"},
        {"id":2,"name":"Harry Kane"}
    ]
@router.get("/", response_model=List[Dict[str,Any]])
def get_authors():
    return author_service.get_all_authors()

@router.get("/{author_id}", response_model=Dict[str, Any])
def get_author(author_id: int):
    return author_service.get_author_by_id(author_id)

@router.post("/", response_model=Dict[str, Any])
def create_author(author_data:AuthorCreate):
    return author_service.create_author(author_data)

@router.put("/{author_id}", response_model=Dict[str, Any])
def update_author(author_id:int, author_data:AuthorUpdate):
    return author_service.update_author(author_id, author_data)


@router.delete("/{author_id}", response_model=Dict[str, Any])
def delete_author(author_id:int):
    return author_service.delete_author(author_id)