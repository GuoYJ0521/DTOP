from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, logout_user, current_user
from .forms import FormLogin, FormRegister
from .code import *
from .models import User

# login
@main.route('/', methods=["GET", "POST"])
def index():
    form = FormLogin()
    if request.method == "POST":
        form_login()
    return render_template("index.html", form=form)

# register
@main.route("/register", methods=['GET', 'POST'])
def register():
    form = FormRegister()
    form_register()
    return render_template("register.html", form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# machine types
@main.route('/machines')
def machines_nav():
    return get_machines()

# 所有機台資訊
@main.route("/machines/<int:id>")
def machines_nav_li(id):
    return get_machines_id(id)

# 單一機台資訊
@main.route("/machine/<int:id>")
def machine_info(id):
    return get_machine_id(id)

# 所有感測器
@main.route("/sensors")
def sensors():
    return get_sensors()

# 機台感測器
@main.route("/machine/sensors/<int:id>")
def machine_sensors(id):
    return get_machine_sensors(id)

# channel資訊
@main.route("/machine/channels/<id>", methods=["GET", "POST"])
def machine_channel(id):
    if request.method == "GET":
        return get_channel_datas(id)
    elif request.method == "POST":
        return post_channel_data(id)

# machine info
@main.route("/machine/<machine>/<machine_id>")
@login_required
def machine(machine, machine_id):
    return render_template("machine.html", user=current_user, machine_id=machine_id)

# log infomation
@main.route("/log", methods=["POST"])
def log():
    return logging()

# mailtrap
@main.route("/message", methods=["POST"])
def message():
    msg_recipients = [user.email for user in User.query.all()]
    mail_message(msg_recipients)
    return {"message": "send"}