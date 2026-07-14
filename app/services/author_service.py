from fastapi import HTTPException, status
from typing import List, Dict, Any
from app.schemas.authors import AuthorCreate, AuthorUpdate

# Giả lập bảng Tác giả trong RAM
authors_mock: List[Dict[str, Any]] = [
    {"id": 1, "name": "Robert C. Martin"},
    {"id": 2, "name": "Eric Matthes"}
]

class AuthorService:
    def get_all_authors(self) -> List[Dict[str, Any]]:
        return authors_mock

    def get_author_by_id(self, author_id: int) -> Dict[str, Any]:
        for author in authors_mock:
            if author["id"] == author_id:
                return author
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Author not found"
        )

    def create_author(self, author_data: AuthorCreate) -> Dict[str, Any]:
        # NGHIỆP VỤ: Kiểm tra trùng tên tác giả (không phân biệt hoa thường)
        for author in authors_mock:
            if author["name"].lower() == author_data.name.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This author already exists"
                )
                
        new_id = authors_mock[-1]["id"] + 1 if authors_mock else 1
        new_author = {
            "id": new_id,
            "name": author_data.name
        }
        authors_mock.append(new_author)
        return new_author

    def update_author(self, author_id: int, author_data: AuthorUpdate) -> Dict[str, Any]:
        for author in authors_mock:
            if author["id"] == author_id:
                update_data = author_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    author[key] = value
                return author
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Author not found"
        )

    def delete_author(self, author_id: int) -> Dict[str, Any]:
        for index, author in enumerate(authors_mock):
            if author["id"] == author_id:
                return authors_mock.pop(index)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Author not found"
        )

author_service = AuthorService()