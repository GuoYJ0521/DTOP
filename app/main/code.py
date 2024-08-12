from flask import request, flash, redirect, url_for, jsonify
from flask import current_app as app
from flask_login import login_user
from flask_mail import Message
from app import db, mail
from . import main
from .models import User, Machines, SensorList, Sensors, Channel, MachineList

def form_login():
    email = request.form['email']
    password = request.form['password']
    remember_me = 'remember_me' in request.form

    user = db.session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user, remember=remember_me)
    else:
        flash("Wrong Email or Password", category="danger")

def form_register():
    if request.method == 'POST':
        user = User(
            name = request.form['username'],
            email = request.form['email'],
            pwd = request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully, please login", category="success")
        return redirect(url_for("main.index"))

# 獲取nav機台
def get_machines():
    machine_list = db.session.query(MachineList).all()
    res = [machine.to_dict() for machine in machine_list]
    return jsonify(res)

# 所有機台資訊
def get_machines_id(id):
    machines = db.session.query(Machines).filter(Machines.machine_id == id).all()
    res = [machine.to_dict() for machine in machines]
    return jsonify(res)

# 單一機台資訊
def get_machine_id(id):
    machine = db.session.query(Machines).filter(Machines.id == id).first()
    res = machine.to_dict()
    return jsonify(res)

# 所有sensor
def get_sensors():
    sensors = db.session.query(SensorList).all()
    res = [sensor.to_dict() for sensor in sensors]
    return jsonify(res)

# 機台所有sensor
def get_machine_sensors(id):
    sensors = db.session.query(Sensors).filter(Sensors.machine == id).all()
    res = [sensor.to_dict() for sensor in sensors]
    return jsonify(res)

# channel 資料
def get_channel_datas(id):
    datas = db.session.query(Channel).filter(Channel.channel==id).order_by(Channel.time.desc()).limit(30).all()
    # res = [data.to_dict() for data in datas]
    res = [data.to_dict() for data in reversed(datas)]

    return jsonify(res)

# log message
def logging():
    try:
        sensor = request.json.get('sensor')
        location = request.json.get('location')
        alert = request.json.get('alert')
        warning = f"異常-{location}{sensor} 建議-{alert}"
        app.logger.warning(warning)
        return jsonify({"error": 0})
    except Exception as e:
        return jsonify({"error": e})

# mail message 收件者，格式為list，否則報錯
def mail_message(msg_recipients):
    try:
        msg_title = 'DT alert'
        msg_sender = 'yijunguo473@gmail.com'
        #  郵件內容
        sensor = request.json.get('sensor')
        location = request.json.get('location')
        alert = request.json.get('alert')
        msg_body = f"異常-{location}{sensor}\n建議-{alert}"
        msg = Message(msg_title,
                    sender=msg_sender,
                    recipients=msg_recipients)
        msg.body = msg_body
        # 寄出郵件
        mail.send(msg)
        return jsonify({"error": 0})
    
    except Exception as e:
        return jsonify({"error": e})

# 上傳channel資料
def post_channel_data(channel):
    try:
        datas = datas = request.json
        new_message = Channel(
            channel=float(channel),
            mean=float(datas["mean"]),
            rms=float(datas["rms"]),
            std=float(datas["std"]),
            fft_1=float(datas["fft_1"]),
            fft_2=float(datas["fft_2"]),
            fft_3=float(datas["fft_3"]),
            fft_4=float(datas["fft_4"]),
            fft_5=float(datas["fft_5"]),
            fft_6=float(datas["fft_6"]),
            fft_7=float(datas["fft_7"]),
            fft_8=float(datas["fft_8"]),
            time=datas["time"]
        )
        with app.app_context():
            db.session.add(new_message)
            db.session.commit()
        return jsonify({"error": 0})

    except Exception as e:
        return jsonify({"error": e})