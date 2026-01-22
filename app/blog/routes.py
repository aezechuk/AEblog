from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.models import Post, generate_unique_slug
from app.blog.forms import PostForm

bp = Blueprint("blog", __name__)


@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)

    posts = db.paginate(Post.query.filter(Post.published == True, Post.slug.isnot(None))
        .order_by(Post.timestamp.desc()),
        page=page,
        per_page=5,
        error_out=False
    )

    next_url = url_for('blog.blog', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blog.blog', page=posts.prev_num) if posts.has_prev else None
    return render_template('blog/index.html', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/blog/<slug>')
def post_detail(slug):
    post = (Post.query.filter(Post.slug==slug, Post.published == True).first_or_404())

    return render_template('blog/post.html', post=post)

@bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per hour")
def new_blog_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            summary=form.summary.data,
            body=form.body.data,
            slug=generate_unique_slug(form.title.data),
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post is live!')
        return redirect(url_for('blog.blog'))

    return render_template('blog/new.html', form=form)

@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per hour")
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if post.author != current_user:
        abort(403)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        if post.title != form.title.data:
            post.slug = generate_unique_slug(form.title.data)
        
        post.title = form.title.data
        post.summary = form.summary.data
        post.body = form.body.data

        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('blog.post_detail', slug=post.slug))

    return render_template('blog/edit.html', form=form, post=post)

@bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
@limiter.limit("10 per hour")
def delete_post(id):
    post = Post.query.get_or_404(id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')

    return redirect(url_for('main.index'))
