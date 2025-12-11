def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    