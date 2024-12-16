from . import post_bp
from flask import render_template, abort, flash, redirect, session, url_for, current_app
from .forms import PostForm
from datetime import datetime
from app.posts.models import Post
from app import db

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get('username', 'Aron')
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=author
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f'Post "{form.title.data}" added successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template("add_post.html", form=form)

@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template("detail_post.html", post=post)

@post_bp.route('/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('.get_posts'))

@post_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('.detail_post', id=post.id))
    return render_template("edit_post.html", form=form, post=post)