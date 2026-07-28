def test_register_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "role": "student",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "student"

def test_login_user(client):
    # 1. Đăng ký user
    client.post(
        "/users/",
        json={
            "username": "testlogin",
            "email": "testlogin@example.com",
            "password": "mypassword",
            "role": "student",
            "is_active": True
        }
    )

    # 2. Đăng nhập thành công
    response = client.post(
        "/auth/login",
        data={"username": "testlogin", "password": "mypassword"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_get_current_user_me(client):
    # 1. Đăng ký & Đăng nhập lấy Token
    client.post(
        "/users/",
        json={
            "username": "me_user",
            "email": "me@example.com",
            "password": "password123",
            "role": "student"
        }
    )
    login_resp = client.post(
        "/auth/login",
        data={"username": "me_user", "password": "password123"}
    )
    token = login_resp.json()["access_token"]

    # 2. Gọi GET /users/me kèm Token
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "me_user"
