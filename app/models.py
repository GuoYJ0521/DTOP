from app import db, login, bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields import EmailField
from flask_login import UserMixin

class MachineList(db.Model):
    __tablename__ = 'machine_list'
    id = db.Column(db.Integer, primary_key=True)
    machine = db.Column(db.String(30))

class Machines(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    machine_id = db.Column(db.Integer)
    location = db.Column(db.String(30))
    work_piece = db.Column(db.String(30))
    cutting_tool = db.Column(db.String(30))
    machine_type = db.Column(db.String(30))

# sensor list
class SensorList(db.Model):
    __tablename__ = 'sensor_list'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    contacts = db.relationship('Sensors',backref='snesortype')

    def __repr__(self) -> str:
        return f'{self.type}'
    
class Sensors(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer,db.ForeignKey(SensorList.id))
    machine = db.Column(db.Integer)
    channel_id = db.Column(db.Integer)
    location = db.Column(db.String(30))
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    location_z = db.Column(db.Float)
    safelimit_mean = db.Column(db.Float)
    safelimit_rms = db.Column(db.Float)
    safelimit_std = db.Column(db.Float)

    def __repr__(self) -> str:
        return f'{self.id, self.sensor_id, self.channel_id, self.location, self.location_x, self.location_y, self.location_z, self.safelimit_mean, self.safelimit_rms, self.safelimit_std}'

class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Float)
    mean = db.Column(db.Float)
    rms = db.Column(db.Float)
    std = db.Column(db.Float)
    fft_1 = db.Column(db.Float)
    fft_2 = db.Column(db.Float)
    fft_3 = db.Column(db.Float)
    fft_4 = db.Column(db.Float)
    fft_5 = db.Column(db.Float)
    fft_6 = db.Column(db.Float)
    fft_7 = db.Column(db.Float)
    fft_8 = db.Column(db.Float)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f'{self.channel, self.mean, self.rms, self.std, self.fft_1, self.fft_2, self.fft_3, self.fft_4, self.fft_5, self.fft_6, self.fft_7, self.fft_8, self.time}'
    
class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    pwd_hash = db.Column(db.String(30))

    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')
    
    # 密碼加密
    @pwd.setter
    def pwd(self, password):
        self.pwd_hash = bcrypt.generate_password_hash(password).decode('utf8')

    # 檢查密碼
    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwd_hash, password)

    def __repr__(self):
        return f'{self.id, self.email, self.name, self.pwd_hash}'

@login.user_loader  
def load_user(user_id):  
    return User.query.get(int(user_id))

# form
class PropertyForm(FlaskForm):
    property1 = StringField("property1",validators=[DataRequired()])
    property2 = StringField("property2",validators=[DataRequired()])
    property3 = StringField("property3",validators=[DataRequired()])
    property4 = StringField("property4",validators=[DataRequired()])
    submit = SubmitField("submit")

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
        validators.Length(10, 30)
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