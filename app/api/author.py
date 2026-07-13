from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)
FAKE_AUTHORS= [
        {"id":1,"name":"Harry Maguire"},
        {"id":2,"name":"Harry Kane"}
    ]
@router.get("/")
def get_authors():
    return FAKE_AUTHORS

@router.get("/{author_id}")
def get_author(author_id: int):
    for author in FAKE_AUTHORS:
        if author["id"]==author_id:
            return author
    raise HTTPException(status_code=404, detail="author not found")
@router.post("/")
def create_author(author_data:dict):
    new_id=FAKE_AUTHORS[-1]["id"]+1 if FAKE_AUTHORS else 1
    new_author={
        "id":new_id,
        "name":author_data.get("name")
    }
    FAKE_AUTHORS.append(new_author)
    return {"message":"author create successfully", "author":new_author}
@router.put("/{author_id}")
def update_author(author_id:int, author_data:dict):
    for author in FAKE_AUTHORS:
        if author["id"]==author_id:
            author["name"]=author_data.get("name")
            return {"message":"author updates successfully", "author":author}
    raise HTTPException(status_code=404, detail="author not found")
@router.delete("/{author_id}")
def delete_author(author_id:int):
    for index, author in enumerate(FAKE_AUTHORS):
        if author["id"]==author_id:
            FAKE_AUTHORS.pop(index)
            return {"message":"author deletes successfully"}
    raise HTTPException(status_code=404, detail="author not found")