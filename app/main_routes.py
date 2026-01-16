from flask import Blueprint, request, render_template, url_for
from app.extensions import db
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.models import Post
from datetime import datetime, timezone

bp = Blueprint("main", __name__)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/')
@bp.route('/index')
def index():
    latest_posts = (Post.query.filter(Post.published ==True, Post.slug.isnot(None))
                    .order_by(Post.timestamp.desc()).limit(3).all())
    return render_template('index.html', title='Home', latest_posts=latest_posts)


    
@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=None)

