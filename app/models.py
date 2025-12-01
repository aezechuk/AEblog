from datetime import datetime, timezone
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
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class Post(db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body}>'