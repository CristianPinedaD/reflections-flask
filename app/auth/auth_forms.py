from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField 
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app import db
from app.main.models import User
from flask_login import current_user
import sqlalchemy as sqla

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
            query = sqla.select(User).where(User.username == username.data)
            user = db.session.scalars(query).first()
            if user is not None: 
                if user.id != current_user.id:
                    raise ValidationError('The username already exists! Please use a different username.')
                    
                    
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')
    
    # def validate_exists(self, username):
    #     query = sqla.select(User).where(User.username == username.data)
    #     user = db.session.scalars(query).first()
    #     if user is None:
    #         raise ValidationError('This user does not exist. ')
