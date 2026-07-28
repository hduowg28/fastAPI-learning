def get_admin_token(client):
    client.post(
        "/users/",
        json={
            "username": "admin_user",
            "email": "admin@example.com",
            "password": "adminpassword",
            "role": "admin"
        }
    )
    login_resp = client.post(
        "/auth/login",
        data={"username": "admin_user", "password": "adminpassword"}
    )
    return login_resp.json()["access_token"]

def test_create_author_and_category(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Tạo Author
    author_resp = client.post("/authors/", json={"name": "Nguyen Nhat Anh"}, headers=headers)
    assert author_resp.status_code == 201
    assert author_resp.json()["name"] == "Nguyen Nhat Anh"

    # Tạo Category
    cat_resp = client.post("/categories/", json={"name": "Tieu Thuyet", "description": "Tieu thuyet van hoc"}, headers=headers)
    assert cat_resp.status_code == 201
    assert cat_resp.json()["name"] == "Tieu Thuyet"

def test_create_book(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Tạo Author & Category trước
    author_id = client.post("/authors/", json={"name": "Nam Cao"}, headers=headers).json()["id"]
    category_id = client.post("/categories/", json={"name": "Truyen Ngan", "description": "Van hoc truyen ngan"}, headers=headers).json()["id"]

    # Tạo Book
    book_resp = client.post(
        "/books/",
        json={
            "title": "Chi Pheo",
            "author_id": author_id,
            "category_id": category_id,
            "published_year": 1941,
            "quantity": 5
        },
        headers=headers
    )
    assert book_resp.status_code == 201
    data = book_resp.json()
    assert data["title"] == "Chi Pheo"
    assert data["quantity"] == 5
    assert data["available_quantity"] == 5

def test_get_books_search_and_pagination(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    author_id = client.post("/authors/", json={"name": "Tolkien"}, headers=headers).json()["id"]
    category_id = client.post("/categories/", json={"name": "Fantasy", "description": "Fantasy novels"}, headers=headers).json()["id"]

    client.post(
        "/books/",
        json={
            "title": "The Hobbit",
            "author_id": author_id,
            "category_id": category_id,
            "published_year": 1937,
            "quantity": 3
        },
        headers=headers
    )

    # Tìm kiếm theo title
    search_resp = client.get("/books/?title=Hobbit")
    assert search_resp.status_code == 200
    results = search_resp.json()
    assert len(results) == 1
    assert results[0]["title"] == "The Hobbit"
