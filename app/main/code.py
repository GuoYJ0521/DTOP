from flask import request, flash, redirect, url_for, current_app, jsonify
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

# sensor data
def get_machine_sensor(machine_id):
    curr_machine = db.session.query(Machines).filter(Machines.id==machine_id).first()
    sensor_list = get_sensor(machine_id)
    result = {"name": curr_machine.name, 
              "type": curr_machine.machine_type, 
              "location": curr_machine.location,
              "work_piece": curr_machine.work_piece,
              "cutting_tool": curr_machine.cutting_tool,
              "sensor_list": sensor_list,
              "stl": "grinder.STL",
              "sensor_stl": "sensor.STL"
              }
    return result

def get_channel(channel_id):
    channel_data = db.session.query(Channel).with_entities(Channel.time, Channel.mean, Channel.std, Channel.rms).filter(Channel.channel==channel_id).order_by(Channel.time.desc()).limit(30).all()
    result = [{'time': row.time.isoformat(), 'mean':row.mean, 'std':row.std, 'rms':row.rms} for row in channel_data]
    return result

def get_sensor(machine_id):
    result = {}
    sensor_list = db.session.query(SensorList).all()
    for type in sensor_list:
        sensors = db.session.query(Sensors).filter(Sensors.sensor_id==type.id, Sensors.machine==machine_id).all()
        list = {}
        for sensor in sensors:
            channel_data = get_channel(sensor.channel_id)
            list[f"{sensor.channel_id}"] = {"id": sensor.id,
                         "location": sensor.location,   
                         "location_x":sensor.location_x,
                         "location_y":sensor.location_y,
                         "location_z":sensor.location_z,
                         "channel_id":sensor.channel_id,
                         "safelimit_mean": sensor.safelimit_mean,
                         "safelimit_rms": sensor.safelimit_rms,
                         "safelimit_std": sensor.safelimit_std,
                         "data": channel_data,
                         "isdanger": False
                         }
        result[f"{type.type}"] = list
    return result

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
    sensor = request.json.get('sensor')
    location = request.json.get('location')
    alert = request.json.get('alert')
    warning = f"異常-{location}{sensor} 建議-{alert}"
    current_app.logger.warning(warning)

# mail message 收件者，格式為list，否則報錯
def mail_message(msg_recipients):
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