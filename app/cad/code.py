from app import db
from flask import jsonify
from .models import WorkingData

def get_controller(id):
    datas = db.session.query(WorkingData).filter(WorkingData.machine_id == id).order_by(WorkingData.time.desc()).first()
    res = datas.to_dict()
    return jsonify(res)
