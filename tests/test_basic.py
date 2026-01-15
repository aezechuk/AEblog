from app import db
from app.models import User, Post


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

def test_logout_redirects_home(client):
    # Create user
    with client.application.app_context():
        user = User(username="tester", email="tester@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    # Log in with correct credentials
    login_response = client.post("/login",
                data={"username": "tester", "password": "password"},
                follow_redirects=True)
    
    assert login_response.status_code == 200
    assert b"Invalid username or password" not in login_response.data

    
    # Log out
    response = client.get("/logout", follow_redirects=True)

    # Should be redirected back to homepage
    assert response.status_code == 200
    assert b"Home - AE's Blog" in response.data # Anchor phrase

def test_logged_in_user_create_post(client):
    # Create user
    with client.application.app_context():
        user = User(username="tester", email="tester@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    # Log in
    login_response = client.post("/login",
                data={"username": "tester", "password": "password"},
                follow_redirects=True)
    
    assert b"Invalid username or password" not in login_response.data

    # Create a post
    response = client.post(
        "/blog/new",
        data={"title": "Test", "summary": "Test post.", "body": "This is a test post.", "published": True},
        follow_redirects=True)

    # Assert Success
    assert response.status_code == 200
    assert b"Test" in response.data

def test_new_post(client):
    # Create user
    with client.application.app_context():
        user = User(username="tester", email="tester@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    # Log in
    login_response = client.post("/login",
                data={"username": "tester", "password": "password"},
                follow_redirects=True)
    
    assert b"Invalid username or password" not in login_response.data

    # Create a post
    post_response = client.post(
        "/blog/new",
        data={"title": "Title of Test Post", "summary": "Summary of a test post.", "body": "Body of a test post."},
        follow_redirects=True)
    
    # Load blogs listing page
    response = client.get("/blog")

    assert response.status_code == 200
    assert b"Title of Test Post" in response.data
    assert b"Summary of a test post." in response.data

def test_new_post_requires_login(client):
    # Try to access the protected route without logging in
    response = client.get("/blog/new", follow_redirects=True)

    # Should redirect to login page
    assert response.status_code == 200
    assert b"Sign In" in response.data # 'Sign-In' header in login.hmtl

def test_slugify(client):
    # Create user
    with client.application.app_context():
        user = User(username="tester", email="tester@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    # Log in
    login_response = client.post("/login",
                data={"username": "tester", "password": "password"},
                follow_redirects=True)
    
    assert b"Invalid username or password" not in login_response.data

    # Create a post
    post_response = client.post(
        "/blog/new",
        data={"title": "Title of Test Post", "summary": "Summary of a test post.", "body": "Body of a test post."},
        follow_redirects=True)
    
    # Retrieve the created post from the database
    with client.application.app_context():
        post = Post.query.filter_by(title="Title of Test Post").first()
        assert post is not None

        # Check that slug was generated correctly
        assert post.slug == "title-of-test-post"

    # Now hit the post detail page using the slug
    response = client.get(f"/blog/{post.slug}")                                    

    assert response.status_code == 200
    assert b"Title of Test Post" in response.data
    assert b"Summary of a test post." in response.data

def test_slug_collision(client):
    # Create User
    with client.application.app_context():
        user = User(username="tester", email="tester@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    # Login
    client.post("/login",
                data={"username": "tester", "password": "password"},
                follow_redirects=True)
    
    # Create first post
    client.post("/blog/new",
                data={"title": "Collision Test",
                      "summary": "First post summary",
                      "body": "First post body"},
                      follow_redirects=True)
    
    # Create second post with same title
    client.post("/blog/new",
                data={"title": "Collision Test",
                      "summary": "Second post summary",
                      "body": "Second post body"},
                      follow_redirects=True) 
    # Retrieve posts
    with client.application.app_context():
        posts = Post.query.filter_by(title="Collision Test").order_by(Post.id).all()

        assert len(posts) == 2

        slug1 = posts[0].slug
        slug2 = posts[1].slug

        assert slug1 == "collision-test"
        assert slug2 != slug1
        assert slug2.startswith("collision-test-")