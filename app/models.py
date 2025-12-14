from app import login, db, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from markdown import markdown
import bleach
from slugify import slugify

followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # always present, integer primary key
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # required string
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # required string
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # not required can be none (before user sets password)
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # generate and store the password hash for the user

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Return True if the given password matches the stored hash
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    # Queries for following, unfollowing counting followers/ing users
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)
    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    # Query for following posts
    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

class Post(db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    slug: so.Mapped[str] = so.mapped_column(
        sa.String(160),
        unique=True,
        index=True,
    )
    summary: so.Mapped[str | None] = so.mapped_column(sa.String(300))
    body: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    body_html: so.Mapped[str] = so.mapped_column(sa.Text)
    published: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True, index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title or self.id}>'

def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    # Query inside loop to ensure uniqueness
    while db.session.scalar(sa.select(Post).where(Post.slug == slug)) is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
    'p', 'pre', 'code', 'blockquote',
    'h1', 'h2', 'h3', 'h4',
    'ul', 'ol', 'li',
    'strong', 'em'
})

def render_body_html(target, value, oldvalue, initiator):
    target.body_html = bleach.clean(
        markdown(value, extensions=['fenced_code', 'codehilite']),
        tags=allowed_tags,
        strip=True
    )
db.event.listen(Post.body, 'set', render_body_html)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

