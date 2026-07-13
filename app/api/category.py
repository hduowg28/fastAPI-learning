from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
FAKE_CATEGORY=[
        {"id":1,"name":"Programming", "description":"Books about software development"},
        {"id":2, "name":"Fiction","description":"Literature and novels"}
    ]
@router.get("/")
def get_categories():
    return FAKE_CATEGORY

@router.get("/{category_id}")
def get_category(category_id: int):
    for category in FAKE_CATEGORY:
        if category["id"]==category_id:
            return category
    raise HTTPException(status_code=404, detail="category not found")

@router.post("/")
def create_categories(category_data:dict):
    new_id=FAKE_CATEGORY[-1]["id"] + 1 if FAKE_CATEGORY else 1
    new_category={
        "id":new_id,
        "name":category_data.get("name"),
        "description":category_data.get("description")
    }
    FAKE_CATEGORY.append(new_category)
    return {"message":"category create successfully", "category":new_category}

@router.put("/{category_id}")
def update_category(category_id:int, category_data:dict):
    for category in FAKE_CATEGORY:
        if category["id"]==category_id:
            category["name"]=category_data.get("name")
            category["description"]=category_data.get("description")
            return {"message":"category update successfully", "category": category}
    raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/{category_id}")
def delete_category(category_id:int):
    for index, category in enumerate(FAKE_CATEGORY):
        if category["id"]==category_id:
            FAKE_CATEGORY.pop(index)
            return {"message":"category deletes successfully"}
    raise HTTPException(status_code=404, detail="category not found")