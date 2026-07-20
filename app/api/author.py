from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.authors import AuthorCreate, AuthorUpdate, AuthorResponse
from app.models.author import Author

# Import class và hàm dependency từ file service
from app.services.author_service import AuthorService, get_author_service

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.get("/", response_model=List[AuthorResponse])
def get_authors(service: AuthorService = Depends(get_author_service)):
    return service.get_all_authors()

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    return service.get_author_by_id(author_id)

@router.post("/", response_model=AuthorResponse)
def create_author(author_data: AuthorCreate, service: AuthorService = Depends(get_author_service)):
    return service.create_author(author_data)

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author_data: AuthorUpdate, service: AuthorService = Depends(get_author_service)):
    return service.update_author(author_id, author_data)

@router.delete("/{author_id}", response_model=AuthorResponse)
def delete_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    return service.delete_author(author_id)