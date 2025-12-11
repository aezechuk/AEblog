from app import db
from app.models import User


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

def test_login_valid_credentials(client):
    # Create test user inside an app context
    with client.application.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("correctpassword")
        db.session.add(user)
        db.session.commit()

    # Log in with correct credentials
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "correctpassword"},
        follow_redirects=True)
    
    # Page should show the user is logged in
    assert response.status_code == 200
    assert b"testuser" in response.data