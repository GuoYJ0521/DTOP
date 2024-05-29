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
@main.route('/get_machines_data', methods=['POST'])
def get_machines_data():
    machine_list = get_machines()
    return jsonify(machine_list)

# machine info
@main.route("/machine/<machine>/<machine_id>")
@login_required
def machine_info(machine, machine_id):
    curr_machine = get_machine_sensor(machine_id)
    return render_template("machine.html",machine=machine, curr_machine=curr_machine, user=current_user)

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