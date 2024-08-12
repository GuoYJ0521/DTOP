from app import db
from flask import current_app as app
from flask import jsonify, request
from .models import WorkingData

# 獲取最後一筆資料
def get_controller(id):
    datas = db.session.query(WorkingData).filter(WorkingData.machine_id == id).order_by(WorkingData.time.desc()).first()
    res = datas.to_dict()
    return jsonify(res)

# 上傳資料
def post_controller(id):
    try:
        datas = request.json
        
        new_message = WorkingData(
            machine_id=float(id),
            x=float(datas["x"]),
            y=float(datas["y"]),
            z=float(datas["z"]),
            speed=float(datas["speed"]),
            time=datas["time"]
        )

        with app.app_context():
            db.session.add(new_message)
            db.session.commit()

        return jsonify({"error": 0})

    except Exception as e:
        app.logger.error(f"Error processing MQTT message: {e}")
        return jsonify({"error": e})
