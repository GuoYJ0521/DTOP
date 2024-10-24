from flask import Flask, jsonify
from flask import current_app as app
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_mqtt import Mqtt
import logging
import json
import requests

pymysql.install_as_MySQLdb() #SQLAlchemy預設使用MySQLdb 但python3連接使用pymysql
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login = LoginManager()  
login.login_view = 'login'
mail = Mail()
mqtt = Mqtt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    mqtt.init_app(app)
    process = ["mean", "std", "rms"]
    danger = {}

    # 配置紀錄日誌
    handler1 = logging.FileHandler('logs/app_info.log', encoding='utf-8')  # INFO級別
    handler1.setLevel(logging.INFO)
    formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler1.setFormatter(formatter1)
    app.logger.addHandler(handler1)

    

    # mqtt listening
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            mytopic = 'DT/#'
            mqtt.subscribe(mytopic)
            print("listening on mqtt")
            app.logger.info(f"[mqtt] has subscribed to topic {mytopic}")
        else:
            app.logger.error(f"[mqtt] Connection failed with result code {rc}")

    from .main.models import Sensors, Channel, SensorList, User
    from .cad.models import WorkingData
    @mqtt.on_message()
    def handle_message(client, userdata, message):
        topic = message.topic.split("/")[1]
        try:
            payload = json.loads(message.payload.decode())
            # 感測器資料
            if topic == "channel":
                with app.app_context():
                    sensor = db.session.query(Sensors).filter(Sensors.channel_id == payload['id']).first().to_dict()
                    id = sensor["id"]
                    if any(float(payload[p]) >= float(sensor[f"safelimit_{p}"]) or float(payload[p]) <= float(sensor[f"lowerlimit_{p}"]) for p in process):
                        if id not in danger or not danger[id]:
                            # logging error info
                            try:
                                sensortype = db.session.query(SensorList).filter(SensorList.id == sensor["id"]).first()
                                if sensortype is not None:
                                    sensortype_dict = sensortype.to_dict()  # 確保 sensortype 不為 None
                                    sensor_type = sensortype_dict["type"]
                                    location = sensor["location"]  # 假設 sensor_dict 包含 location
                                    alert = "修整砂輪"
                                    warning = f"異常-{location}{sensor_type} 建議-{alert}"
                                    app.logger.warning(warning)

                            except Exception as e:
                                return jsonify({"error": str(e)})
                            
                            # email寄送
                            try:
                                msg_recipients = User.to_list()
                                msg_title = 'DT alert'
                                # 寄送者
                                msg_sender = 'yijunguo473@gmail.com'
                                #  郵件內容
                                sensor = sensortype_dict["type"]
                                location = sensor["location"]
                                alert = "修整砂輪"
                                msg_body = f"異常-{location}{sensor} 建議-{alert}"
                                msg = Message(msg_title,
                                            sender=msg_sender,
                                            recipients=msg_recipients)
                                msg.body = msg_body
                                # 寄出郵件
                                mail.send(msg)
                            
                            except Exception as e:
                                return jsonify({"error": str(e)})

                    else:
                        danger[id] = False

                # 上傳資料庫
                try:
                    new_message = Channel(
                    channel=float(id),
                    mean=float(payload["mean"]),
                    rms=float(payload["rms"]),
                    std=float(payload["std"]),
                    fft_1=float(payload["fft_1"]),
                    fft_2=float(payload["fft_2"]),
                    fft_3=float(payload["fft_3"]),
                    fft_4=float(payload["fft_4"]),
                    fft_5=float(payload["fft_5"]),
                    fft_6=float(payload["fft_6"]),
                    fft_7=float(payload["fft_7"]),
                    fft_8=float(payload["fft_8"]),
                    time=payload["time"]
                    )
                    with app.app_context():
                        db.session.add(new_message)
                        db.session.commit()

                except Exception as e:
                    return jsonify({"error": str(e)})

            # 控制器資料上傳資料庫
            elif topic == "controller":
                payload = json.loads(message.payload.decode())
                try:
                    new_message = WorkingData(
                        machine_id=float(id),
                        x=float(payload["x"]),
                        y=float(payload["y"]),
                        z=float(payload["z"]),
                        speed=float(payload["speed"]),
                        time=payload["time"]
                    )

                    with app.app_context():
                        db.session.add(new_message)
                        db.session.commit()

                except Exception as e:
                    app.logger.error(f"Error processing MQTT message: {e}")
                    return jsonify({"error": str(e)})

        except Exception as e:
                app.logger.error(f"Error processing MQTT message: {str(e)}")

    # blue-print設定
    from .main import main as main_blueprint
    from .cad import cad as cad_blueprint
    from .fea import fea as fea_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(cad_blueprint, url_prefix="/cad")
    app.register_blueprint(fea_blueprint, url_prefix="/fem")

    return app