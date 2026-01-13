import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
