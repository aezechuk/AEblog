import pytest
from app import app, db

@pytest.fixture
def client():
    app.config.update(TESTING = True,
                      SQLALCHEMY_DATABASE_URI = "sqlite://",
                      WTF_CSRF_ENABLED = False)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# Enables in-memory db, flask-login compatibility, isolated tests