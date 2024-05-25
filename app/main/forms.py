from flask_wtf import FlaskForm
from wtforms.fields import EmailField
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField
from .models import User

# login form
class FormLogin(FlaskForm):
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('remember me')

    submit = SubmitField('Log in')

# register form
class FormRegister(FlaskForm):
    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(1, 10)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    submit = SubmitField('Register New Account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise  validators.ValidationError('UserName already register by somebody')