from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)
FAKE_USERS = [
    {"id": 1, "username": "admin", "email": "admin@library.com", "role": "admin"},
    {"id": 2, "username": "librarian_01", "email": "librarian1@library.com", "role": "librarian"},
    {"id": 3, "username": "student_johndoe", "email": "john@student.com", "role": "student"}
]
@router.get("/")
def get_users():
    return FAKE_USERS
@router.get("/{user_id}")
def get_user(user_id: int):
    for user in FAKE_USERS:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not Found")
@router.post("/")
def create_user(user_data:dict):
    new_id=FAKE_USERS[-1]["id"]+ 1 if FAKE_USERS else 1
    new_user={
        "id":new_id, 
        "username":user_data.get("username","new_user"),
        "email":user_data.get("email","unknown@email.com"),
        "role":user_data.get("role","student")
    }
    FAKE_USERS.append(new_user)
    return {"message":"User created successfully", "user":new_user}

@router.put("/{user_id}")
def update_user(user_id:int, update_data: dict):
    for user in FAKE_USERS:
        if user["id"] ==user_id:
            user["username"]=update_data.get("username", user["username"])
            user["email"]=update_data.get("email", user["email"])
            user["role"]=update_data.get("role", user["role"])
            return {"message":"User updated successfully", "user":user}
    
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(FAKE_USERS):
        if user["id"]==user_id:
            deleted_user=FAKE_USERS.pop(index)
            return {"message":f"User {deleted_user["username"]} delete successfully"}
    raise HTTPException(status_code=404, detail="user not found")
