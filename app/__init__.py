from flask import Flask
from flask import current_app as app
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
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
process = ["mean", "std", "rms"]

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    mqtt.init_app(app)

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

    # from .main.models import Channel
    # from .cad.models import WorkingData
    from .main.models import Sensors
    @mqtt.on_message()
    def handle_message(client, userdata, message):
        topic = message.topic.split("/")[1]
        try:
            payload = json.loads(message.payload.decode())
            if topic == "channel":
                with app.app_context():
                    sensor = db.session.query(Sensors).filter(Sensors.channel_id == payload['id']).first().to_dict()
                    if any(float(payload[p]) >= float(sensor[f"safelimit_{p}"]) or float(payload[p]) <= float(sensor[f"lowerlimit_{p}"]) for p in process):
                        requests.post(f'http://127.0.0.1:5000/message', json={"sensor":sensor["id"], "location":sensor["location"], "alert": "修整砂輪"})
                        requests.post(f'http://127.0.0.1:5000/log', json={"sensor":sensor["id"], "location":sensor["location"], "alert": "修整砂輪"})
                    else:
                        print("safe")
                # response = requests.post(f'http://127.0.0.1:5000/machine/channels/{payload["id"]}', json=payload)

            elif topic == "controller":
                payload = json.loads(message.payload.decode())
                response = requests.post(f'http://127.0.0.1:5000/cad/controller/{payload["id"]}', json=payload)

        except Exception as e:
                app.logger.error(f"Error processing MQTT message: {e}")

    # blue-print設定
    from .main import main as main_blueprint
    from .cad import cad as cad_blueprint
    from .fea import fea as fea_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(cad_blueprint, url_prefix="/cad")
    app.register_blueprint(fea_blueprint, url_prefix="/fem")

    # 配置紀錄日誌
    handler1 = logging.FileHandler('logs/app_info.log', encoding='utf-8')  # INFO級別
    handler1.setLevel(logging.INFO)
    formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler1.setFormatter(formatter1)

    handler2 = logging.FileHandler('logs/app_error.log', encoding='utf-8')  # ERROR級別
    handler2.setLevel(logging.ERROR)
    formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler2.setFormatter(formatter2)

    # app.logger.setLevel(logging.WARNING)
    app.logger.addHandler(handler1)
    app.logger.addHandler(handler2)

    return app