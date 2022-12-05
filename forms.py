from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,DateField ,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea
from models import db, User, ToDo

class AddForm(FlaskForm):
    title=StringField("title",validators=[DataRequired()])
    date_due=DateField("date_due",validators=[DataRequired()])
    description=StringField("description",validators=[DataRequired()], widget=TextArea())
    submit=SubmitField("Submit") 

class LoginForm(FlaskForm):
    username =StringField("Username",validators=[DataRequired()])
    password =PasswordField("Password",validators=[DataRequired()])
    submit =SubmitField("Submit")  

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    password_hash=PasswordField("Password",validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match'), Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    password_hash2=PasswordField("Confirm Password",validators=[DataRequired(), Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    submit=SubmitField("Submit")

    def validate_username(self,username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists")

class PasswordForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password_hash=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit")                  