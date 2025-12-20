from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main.models import Post, User, Admin
from app.main.forms import PostForm
from datetime import datetime, timezone
from flask_login import current_user, logout_user, login_required
from app.main.decorators import is_admin
from app.main import main_blueprint as bp_main 

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    posts = db.session.scalars(sqla.select(Post)).all()
    
    return render_template('index.html', title="Posts", posts = posts, user=current_user)
    
@bp_main.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    pform = PostForm()
    if pform.validate_on_submit():
        newpost = Post(
            name = pform.title.data, 
            body = pform.body.data, 
            writer_id = current_user.id
        )
        
        db.session.add(newpost)
        db.session.commit()
        flash('Reflection Posted!')
        return redirect(url_for('main.index'))
    return render_template('create.html', title='Post Reflection', form=pform, user=current_user)

@bp_main.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletepost(post_id : int):
    post = db.session.get(Post, post_id)
    if post: 
        db.session.delete(post)
        db.session.commit()
        flash('Post succesfully deleted!')
        return redirect(url_for('main.index'))
    flash('Post not found!')
    return redirect(url_for('main.index'))