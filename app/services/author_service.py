from fastapi import HTTPException, status, Depends
from typing import List, Dict, Any
from app.schemas.authors import AuthorCreate, AuthorUpdate
from app.repositories.author_repository import AuthorRepository
from app.models.author import Author
from sqlalchemy.orm import Session
from app.core.database import get_db

class AuthorService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthorRepository(db)

    def get_all_authors(self) -> List[Author]:
        return self.repo.get_all()

    def get_author_by_id(self, author_id: int) -> Author:
        author_db = self.repo.get_by_id(author_id)
        if not author_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Author not found"
            )
        return author_db

    def create_author(self, author_data: AuthorCreate) -> Author:
        return self.repo.create(author_data)

    def update_author(self, author_id: int, author_data: AuthorUpdate) -> Author:
        author_db = self.get_author_by_id(author_id) 
        return self.repo.update(author_db, author_data)

    def delete_author(self, author_id: int) -> Author:
        return self.repo.delete(self.get_author_by_id(author_id))

# Hàm dependency cấp Service cho Router gọi tới
def get_author_service(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(db)