def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_login_invalid_credentials(client):
    # attempt login with wrong username/password
    response = client.post("/login",
        data={"username": "wronguser", "password": "wrongpass"},
        follow_redirects=True)

    # The page should load, but login should fail
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data