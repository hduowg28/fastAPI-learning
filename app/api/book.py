from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)
FAKE_BOOKS=[
        {"id":1, "title":"clean code"},
        {"id":2, "title":"Python Crash Course"}
    ]
@router.get("/")
def get_books():
    return FAKE_BOOKS
@router.get("/{book_id}")
def get_book(book_id: int):
    for book in FAKE_BOOKS:
        if book["id"]==book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/")
def create_book(book_data:dict):
    new_id=FAKE_BOOKS[-1]["id"]+1 if FAKE_BOOKS else 1
    new_book={
        "id":new_id, 
        "title":book_data.get("title")
    }
    FAKE_BOOKS.append(new_book)
    return {"message":"book created successfully", "book":new_book}

@router.put("/{book_id}")
def update_book(book_id:int, book_data:dict):
    for book in FAKE_BOOKS:
        if book["id"]==book_id:
            book["title"]=book_data.get("title", book["title"])
            return {"message":"book updated successfully", "book":book}
    raise HTTPException(status_code=404, detail="book not found")
@router.delete("/{book_id}")
def delete_book(book_id:int):
    for index, book in enumerate(FAKE_BOOKS):
        if book["id"]==book_id:
            FAKE_BOOKS.pop(index)
            return {"message":"book deleted successfully"}
    raise HTTPException(status_code=404, detail="book not found")