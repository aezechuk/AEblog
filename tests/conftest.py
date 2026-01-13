import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app, db

@pytest.fixture
def client():
    app.config.update(TESTING = True,
                      SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:",
                      WTF_CSRF_ENABLED = False)

    
    with app.app_context():
        db.engines.clear()  # forces old connection to drop and create new one
        db.create_all()
        
        with app.test_client() as client:
            yield client

        db.drop_all()

# Enables in-memory db, flask-login compatibility, isolated tests