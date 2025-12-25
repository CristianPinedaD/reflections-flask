from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import  ValidationError, DataRequired, InputRequired, Email, Length, NumberRange, EqualTo, Optional
from app import db
import sqlalchemy as sqla
from app.main.models import User

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post Reflection')
    
class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Edit User')



            
    