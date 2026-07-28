from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.schemas.authors import AuthorCreate, AuthorUpdate, AuthorResponse
from app.models.author import Author
from app.services.author_service import AuthorService, get_author_service
from app.core.security import require_roles

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

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin", "librarian"))])
def create_author(author_data: AuthorCreate, service: AuthorService = Depends(get_author_service)):
    return service.create_author(author_data)

@router.put("/{author_id}", response_model=AuthorResponse, dependencies=[Depends(require_roles("admin", "librarian"))])
def update_author(author_id: int, author_data: AuthorUpdate, service: AuthorService = Depends(get_author_service)):
    return service.update_author(author_id, author_data)

@router.delete("/{author_id}", response_model=AuthorResponse, dependencies=[Depends(require_roles("admin", "librarian"))])
def delete_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    return service.delete_author(author_id)