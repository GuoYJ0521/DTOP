from flask import Flask, current_app
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_mqtt import Mqtt
import logging
import json

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

    from .main.models import Channel
    from .cad.models import WorkingData
    @mqtt.on_message()
    def handle_message(client, userdata, message):
        topic = message.topic.split("/")[1]
        # print(topic)

        if topic == "channel":
            try:
                datas = json.loads(message.payload.decode())
                app.logger.info("[mqtt] received data")
                new_message = Channel(
                    channel=int(datas["id"]),
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
            except Exception as e:
                app.logger.error(f"Error processing MQTT message: {e}")

        if topic == "controller":
            try:
                datas = json.loads(message.payload.decode())
                new_message = WorkingData(
                    machine_id = int(datas["id"]),
                    x = float(datas["x"]),
                    y = float(datas["y"]),
                    z = float(datas["z"]),
                    speed = float(datas["speed"]),
                )
                with app.app_context():
                    db.session.add(new_message)
                    db.session.commit()
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