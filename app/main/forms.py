from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import  ValidationError, DataRequired, InputRequired, Email, Length, NumberRange, EqualTo, Optional

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post Reflection')