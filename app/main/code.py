from flask import request, flash, redirect, url_for, jsonify, session
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