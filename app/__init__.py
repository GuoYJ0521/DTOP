from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_mqtt import Mqtt
import logging

pymysql.install_as_MySQLdb() #SQLAlchemy預設使用MySQLdb 但python3連接使用pymysql
db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()  
login.login_view = 'login'
mail = Mail()
mqtt = Mqtt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    mqtt.init_app(app)

    from .main import main as main_blueprint
    from .cad import cad as cad_blueprint
    from .fea import fea as fea_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(cad_blueprint, url_prefix="/cad")
    app.register_blueprint(fea_blueprint, url_prefix="/fem")

    # 配置紀錄日誌
    handler1 = logging.FileHandler('logs/app_info.log', encoding='utf-8')  # INFO級別
    handler1.setLevel(logging.DEBUG)
    formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler1.setFormatter(formatter1)

    handler2 = logging.FileHandler('logs/app_error.log', encoding='utf-8')  # ERROR級別
    handler2.setLevel(logging.ERROR)
    formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler2.setFormatter(formatter2)

    app.logger.setLevel(logging.WARNING)
    app.logger.addHandler(handler1)
    app.logger.addHandler(handler2)

    return app