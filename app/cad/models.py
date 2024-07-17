from app import db

class WorkingData(db.Model):
    __tablename__ = 'working_data'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)
    speed = db.Column(db.Float)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f'{self.machine_id, self.x, self.y, self.z, self.speed}'
    
    def to_dict(self):
        return {
            "machine_id": self.machine_id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "speed": self.speed,
            "time": self.time
        }