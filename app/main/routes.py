from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, logout_user, current_user
from .forms import FormLogin, FormRegister
from .code import *

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

# 獲取navbar資料
# @main.route('/get_machines_data', methods=['POST'])
# def get_machines_data():
#     machine_list = get_machines()
#     return jsonify(machine_list)

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
@main.route("/machine/channels/<id>")
def machine_channel(id):
    return get_channel_datas(id)

# machine info
@main.route("/machine/<machine>/<machine_id>")
@login_required
def machine(machine, machine_id):
    return render_template("machine.html", user=current_user, machine_id=machine_id)

# log infomation
@main.route("/log", methods=["POST"])
def log():
    logging()
    return {"message": "warning"}

# mailtrap
@main.route("/message", methods=["POST"])
def message():
    msg_recipients = [f'{current_user.email}']
    # mail_message(msg_recipients)
    return {"message": "send"}

# 獲取channel資料
@main.route("/get_channel_data", methods=['POST'])
def get_channel_data():
    id = request.json.get('id')
    channel_data = get_channel(id)
    return jsonify(channel_data)