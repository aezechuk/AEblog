from flask import Blueprint, current_app, request, render_template, flash, redirect, url_for, abort 
from flask_login import current_user, login_required
from app.extensions import db 
from app.users.forms import EditProfileForm, EmptyForm

import sqlalchemy as sa 
from app.models import User, Post

bp = Blueprint("users", __name__)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.session.scalar(
        sa.select(User).where(User.username == username))
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).where(Post.user_id == user.id).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('users.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('users.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('users/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'user {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('users.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('index'))
    
@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('users.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('users.user', username=username))
    else:
        return redirect(url_for('index'))