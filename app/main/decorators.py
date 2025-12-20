from functools import wraps 
from flask_login import current_user
from app.main.models import User, Admin
from flask import flash, redirect, url_for

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if (isinstance(current_user, Admin)):
            return func(*args, **kwargs)
        else:
            flash("You need to be an Admin to access this page!")
            return redirect(url_for('main.index'))
            
    return wrapper