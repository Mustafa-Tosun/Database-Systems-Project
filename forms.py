from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField, IntegerField
#from flask.ext.wtf.html5 import NumberInput
from wtforms.validators import DataRequired, Email, Optional, NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    #username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
    realname = StringField("Realname", validators=[Optional()])
    username = StringField("Username", validators=[DataRequired()])
    email1 = EmailField("Email address", validators=[DataRequired(), Email()])
    email2 = EmailField("Email address", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Password", validators=[DataRequired()])

class AuthorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    birth = IntegerField("Birth Year", validators=[Optional()])
    death = IntegerField("Death Year", validators=[Optional()])

class PoemForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional()])
    author = StringField("Author", validators=[DataRequired()])

class CommentForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()])

class VoteForm(FlaskForm):
    point = IntegerField("Rate", validators=[DataRequired()])

class UpdateUserForm(FlaskForm):
    realname = StringField("Realname", validators=[Optional()])