from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_mqtt import Mqtt
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import json

import logging
# logging.basicConfig(filename='logs/app.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

pymysql.install_as_MySQLdb() #SQLAlchemy預設使用MySQLdb 但python3連接使用pymysql
app = Flask(__name__)
app.config.from_object('config.Config')  # 使用配置文件
db = SQLAlchemy(app)
mqtt = Mqtt(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)  
login.login_view = 'login'

# 配置日志记录器
handler1 = logging.FileHandler('logs/app_info.log', encoding='utf-8')  # 用于记录 INFO 级别的日志
handler1.setLevel(logging.DEBUG)
formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler1.setFormatter(formatter1)

handler2 = logging.FileHandler('logs/app_error.log', encoding='utf-8')  # 用于记录 ERROR 级别的日志
handler2.setLevel(logging.ERROR)
formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler2.setFormatter(formatter2)

app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler1)
app.logger.addHandler(handler2)

# mqtt listening
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    try:
        mytopic = 'grinder/#'
        mqtt.subscribe(topic=mytopic)
        print(f"[mqtt] has listen topic {mytopic}")
    except Exception as e:
        print("Error:", e)

from app.models import Channel
@mqtt.on_message()
def handle_message(client, userdata, message):
    datas = json.loads(message.payload.decode())
    try:
        print("[mqtt] recieved data")
        new_message = Channel(id=float(datas["id"]),mean=float(datas["mean"]), rms=float(datas["rms"]), std=float(datas["std"]), fft_1=float(datas["fft_1"]),
                               fft_2=float(datas["fft_2"]), fft_3=float(datas["fft_3"]), fft_4=float(datas["fft_4"]), fft_5=float(datas["fft_5"]),
                                 fft_6=float(datas["fft_6"]), fft_7=float(datas["fft_7"]), fft_8=float(datas["fft_8"]), time=datas["time"])
        with app.app_context():
            db.session.add(new_message)
            db.session.commit()
    except Exception as e:
        print("Error:", e) 

from app import routes # 導入路由