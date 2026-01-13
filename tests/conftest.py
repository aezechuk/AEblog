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
    # Create temp database file
    db_fd, db_path = tempfile.mkstemp()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)
