class Config:
    SECRET_KEY = 'hard to guess string'
    SESSION_PROTECTION = 'strong'
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@hostname/tablename'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_BROKER_URL = 'hostname'
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = 'username'
    MQTT_PASSWORD = 'password'
    MQTT_KEEPALIVE = 5

    # mail
    MAIL_SERVER='live.smtp.mailtrap.io'
    MAIL_PORT='port'
    MAIL_USERNAME='api'
    MAIL_PASSWORD='password'
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False