from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla
from app import db
from app.main.models import Post, User, Admin
from app.main.forms import PostForm, EditProfileForm
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

@bp_main.route('/user/<int:userid>/profile', methods=['GET'])
@login_required
def view_profile(userid: int):
    user = db.session.get(User, userid)
    if user is None:
        flash('User does not exist!')
        return redirect(url_for('main.index'))
    myposts = user.get_posts()
    num_posts = len(myposts)
    return render_template('profile.html', title='View Profile', user=user, num_posts=num_posts, posts=myposts)
    
@bp_main.route('/user/<int:userid>/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile(userid: int):
    user = db.session.get(User, userid)
    if user is None:
        flash('User does not exist!')
        return redirect(url_for('main.index'))
    eform = EditProfileForm()
    eform.name.data = user.get_name()
    eform.username.data = user.get_username()
        
    if eform.validate_on_submit():
        user.name = eform.name.data
        user.username = eform.username.data
        
        db.session.add(user)
        db.session.commit()
        flash('Profile Updated!')
        return redirect(url_for('main.view_profile', userid = user.get_id()))
    
    return render_template('edit_user.html', title='Edit Profile', form=eform)