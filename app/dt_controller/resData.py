from app.models import *
from flask import request
# import tensorflow as tf
# from tensorflow.keras.models import load_model
import time

# machine list
def get_machines():
    data = []
    machine_list = db.session.query(MachineList).all()

    for ml in machine_list:
        list = []
        machines = db.session.query(Machines).filter(Machines.machine_id == ml.id).all()

        for m in machines:
            list.append({"name":m.name,"id":m.id})
        data.append({"type":ml.machine, "list":list})

    return data

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
              "stl": "grinder1.STL",
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

def k_predict():
    property1, property2, property3, property4 = None, None, None, None
    operation = None
    properties = None
    status = 0

    # model = load_model("app/static/test0217.h5")
    form = PropertyForm()
    form.property1.data = 1
    form.property2.data = 2 
    form.property3.data = 3
    form.property4.data = 4

    data = {
        "form": form,
        "operation": operation,
        "properties": properties,
        "status": status
    }

    if form.validate_on_submit():
        property1 = form.property1.data
        property2 = form.property2.data
        property3 = form.property3.data
        property4 = form.property4.data
        properties = [property1,property2,property3,property4]
        form.property1.data = ''
        form.property2.data = '' 
        form.property3.data = ''
        form.property4.data = ''

        # operation = str(model.predict([[int(property1)/10,int(property2)/10,int(property3)/10,int(property4)/10]])[0])
        operation = {"k1": 10, "k2": 5}
        # operation = json.dumps(operation)
        # requests.post("http://localhost:5000/run-abaqus", json=operation)
        status = 1

        data["form"] = form
        data["operation"] = operation
        data["properties"] = properties
        data["status"] = status
    return data

def abaqus_sumit():
    # 获取 POST 请求中的参数
    k1 = request.json.get('k1')
    k2 = request.json.get('k2')

    cwd = r"D:\kevin\DTOP-Kevin\app\static\abaqus"
    inp = "test.inp"
    inp_folder = "inp"
    odb_folder = "odb"

    # try:
    #     os.chdir(os.path.join(cwd,odb_folder))
    #     subprocess.run(f"abaqus job=simulation int input={os.path.join(cwd,inp_folder,inp)} ask_delete=OFF",shell=True)

    # except subprocess.CalledProcessError as e:
    #     print("abaqus error：", e)
    time.sleep(1)
    data = {
        "k1": float(k1-2)*0.8+2,
        "k2": float(k2-2)*0.8+2
    }
    return data