from datetime import date, timedelta

def setup_data(client):
    # 1. Admin đăng ký & đăng nhập
    client.post("/users/", json={"username": "admin_borrow", "email": "admin_b@example.com", "password": "pass", "role": "admin"})
    admin_token = client.post("/auth/login", data={"username": "admin_borrow", "password": "pass"}).json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Student đăng ký & đăng nhập
    student_resp = client.post("/users/", json={"username": "student_borrow", "email": "student_b@example.com", "password": "pass", "role": "student"})
    student_id = student_resp.json()["id"]
    student_token = client.post("/auth/login", data={"username": "student_borrow", "password": "pass"}).json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 3. Tạo Author, Category, Book (quantity=2)
    author_id = client.post("/authors/", json={"name": "Author 1"}, headers=admin_headers).json()["id"]
    category_id = client.post("/categories/", json={"name": "Cat 1", "description": "Desc"}, headers=admin_headers).json()["id"]
    book_id = client.post("/books/", json={"title": "Test Book", "author_id": author_id, "category_id": category_id, "published_year": 2024, "quantity": 2}, headers=admin_headers).json()["id"]

    return {
        "student_id": student_id,
        "student_headers": student_headers,
        "book_id": book_id
    }

def test_borrow_and_return_book_flow(client):
    data = setup_data(client)
    student_id = data["student_id"]
    student_headers = data["student_headers"]
    book_id = data["book_id"]

    today = date.today().isoformat()
    return_day = (date.today() + timedelta(days=7)).isoformat()

    # 1. Mượn sách
    borrow_resp = client.post(
        "/borrows/",
        json={
            "user_id": student_id,
            "book_id": book_id,
            "borrow_date": today,
            "return_date": return_day,
            "status": "Borrowed"
        },
        headers=student_headers
    )
    assert borrow_resp.status_code == 201
    borrow_id = borrow_resp.json()["id"]

    # 2. Kiểm tra available_quantity của Sách đã giảm từ 2 xuống 1
    book_resp = client.get(f"/books/{book_id}")
    assert book_resp.json()["available_quantity"] == 1

    # 3. Trả sách
    return_resp = client.put(
        f"/borrows/{borrow_id}/return",
        headers=student_headers
    )
    assert return_resp.status_code == 200
    assert return_resp.json()["status"] == "returned"

    # 4. Kiểm tra available_quantity của Sách đã tăng từ 1 trở lại 2
    book_after_return = client.get(f"/books/{book_id}")
    assert book_after_return.json()["available_quantity"] == 2
