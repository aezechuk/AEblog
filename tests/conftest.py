import os
import tempfile

db_fd, db_path = tempfile.mkstemp()
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app, db

@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()

