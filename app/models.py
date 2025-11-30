from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # always present, integer primary key
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # required string
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # required string
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # not required can be none (before user sets password)

    def __repr__(self):
        return '<User {}>'.format(self.username)