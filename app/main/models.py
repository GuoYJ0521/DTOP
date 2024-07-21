from flask_login import UserMixin
from app import db, bcrypt, login
from sqlalchemy import DECIMAL

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(30))
    pwd_hash = db.Column(db.String(128))

    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')
    
    # 密碼加密
    @pwd.setter
    def pwd(self, password):
        self.pwd_hash = bcrypt.generate_password_hash(password).decode('utf8')

    # 檢查密碼
    def check_password(self, password):
        print(password, self.pwd_hash)
        return bcrypt.check_password_hash(self.pwd_hash, password)

    def __repr__(self):
        return f'{self.email, self.name, self.pwd_hash}'

@login.user_loader
def load_user(user_id):
    # Return the user object for the given user_id
    return User.query.get(int(user_id))

class MachineList(db.Model):
    __tablename__ = 'machine_list'
    id = db.Column(db.Integer, primary_key=True)
    machine = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'machine': self.machine
        }

class Machines(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    machine_id = db.Column(db.Integer)
    location = db.Column(db.String(30))
    work_piece = db.Column(db.String(30))
    cutting_tool = db.Column(db.String(30))
    machine_type = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'machine_id': self.machine_id,
            'location': self.location,
            'work_piece': self.work_piece,
            'cutting_tool': self.cutting_tool,
            'machine_type': self.machine_type
        }

# sensor list
class SensorList(db.Model):
    __tablename__ = 'sensor_list'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    contacts = db.relationship('Sensors',backref='snesortype')

    def __repr__(self) -> str:
        return f'{self.type}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type
        }
    
class Sensors(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer,db.ForeignKey(SensorList.id))
    machine = db.Column(db.Integer)
    channel_id = db.Column(DECIMAL(2, 1))
    location = db.Column(db.String(30))
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    location_z = db.Column(db.Float)
    safelimit_mean = db.Column(db.Float)
    safelimit_rms = db.Column(db.Float)
    safelimit_std = db.Column(db.Float)

    def __repr__(self) -> str:
        return f'{self.id, self.sensor_id, self.channel_id, self.location, self.location_x, self.location_y, self.location_z, self.safelimit_mean, self.safelimit_rms, self.safelimit_std}'

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "machine": self.machine,
            "channel_id": self.channel_id,
            "location": self.location,
            "location_x": self.location_x,
            "location_y": self.location_y,
            "location_z": self.location_z,
            "safelimit_mean": self.safelimit_mean,
            "safelimit_rms": self.safelimit_rms,
            "safelimit_std": self.safelimit_std
        }

class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(DECIMAL(2, 1))
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
    
    def to_dict(self):
        return {
            "channel": self.channel,
            "mean": self.mean,
            "rms": self.rms,
            "std": self.std,
            # "fft_1": self.fft_1,
            # "fft_2": self.fft_2,
            # "fft_3": self.fft_3,
            # "fft_4": self.fft_4,
            # "fft_5": self.fft_5,
            # "fft_6": self.fft_6,
            # "fft_7": self.fft_7,
            # "fft_8": self.fft_8,
            "time": self.time
        }