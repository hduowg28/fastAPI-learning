from fastapi import APIRouter,HTTPException
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)
FAKE_BORROWS=[
    {
        "id": 1, 
        "user_id": 3, 
        "book_id": 1, 
        "borrow_date": "2026-07-01", 
        "return_date": None, 
        "status": "borrowed"
    }
]
@router.post("/")
def create_borrow(borrow_data: dict):
    new_id = FAKE_BORROWS[-1]["id"] + 1 if FAKE_BORROWS else 1
    borrow_date=datetime.now().strftime("%Y-%m-%d")
    new_borrow={
        "id":new_id, 
        "user_id":borrow_data.get("user_id"),
        "book_id":borrow_data.get('book_id'),
        "borrow_date": borrow_date,
        "return_date":None,
        "status":"borrowed"
    }
    FAKE_BORROWS.append(new_borrow)
    return {"message":"Book borrowed successfully", "borrowed_record":new_borrow}

@router.get("/")
def get_borrows():
    return FAKE_BORROWS

# @router.get("/{borrow_id}")
# def get_borrow(borrow_id: int):
#     for borrow in FAKE_BORROWS:
#         if borrow["id"]==borrow_id:
#             return borrow
#     raise HTTPException(status_code=404, detail=f"borrow information not found by id {borrow_id}")

@router.put("/{borrow_id}")
def return_book(borrow_id:int):
    for borrow in FAKE_BORROWS:
        if borrow["id"]==borrow_id:
            if borrow["status"]=="returned":
                return {"message":"this borrow had returned before"}
            borrow["return_date"]=datetime.now().strftime("%Y-%m-%d")
            borrow["status"]="returned"
            return {"message":"Book returned successfully","borrow":borrow}
    raise HTTPException(status_code=404, detail="borrow record not found")

@router.get("/overdue")
def get_overdue_borrows():
    return [
        {
            "id": 99, 
            "user_id": 3, 
            "book_id": 2, 
            "borrow_date": "2026-05-01", 
            "status": "overdue"
        }
    ]