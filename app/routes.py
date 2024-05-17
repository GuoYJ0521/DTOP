from flask import render_template, jsonify, url_for, redirect, flash
from app import app
from app.dt_controller.resData import *
from flask_login import login_user, login_required, logout_user

# index
@app.route("/")
def index():
    form = FormLogin()
    return render_template("index.html", form=form, errors=form.errors)

# machine info
@app.route("/machine/<machine>/<machine_id>")
@login_required
def machine_info(machine, machine_id):
    # current machine
    curr_machine = get_machine_sensor(machine_id)
    return render_template("machine.html",machine=machine, curr_machine=curr_machine)

# unity model
@app.route("/cad")
@login_required
def cad():
    return render_template("cad.html")

# todo: machine learninng
@app.route("/ai")
@login_required
def ai():
    return render_template("ai.html")

# abaqus finite element analyysis
@app.route("/fem", methods=["GET","POST"])
@login_required
def fem():
    data = k_predict()
    return render_template("fem.html", form=data["form"], operation=data["operation"], properties=data["properties"], status=data["status"])

# register
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = form_register()
    return render_template("register.html", form=form, errors=form.errors)

# api
# 獲取navbar資料
@app.route('/get_machines_data', methods=['POST'])
def get_machines_data():
    machine_list = get_machines()
    return jsonify(machine_list)

# 獲取channel資料
@app.route("/get_channel_data", methods=['POST'])
def get_channel_data():
    id = request.json.get('id')
    channel_data = get_channel(id)
    return jsonify(channel_data)

# run abaqus function
@app.route("/run-abaqus", methods=["POST"])
def run_abaqus_api():
    data = abaqus_sumit()
    return jsonify(data)

# mailtrap
@app.route("/message", methods=["POST"])
def message():
    msg_recipients = ['yijunguo473@gmail.com']
    mail_message(msg_recipients)
    return 'send successfully'

# log infomation
@app.route("/log", methods=["POST"])
def log():
    logging()
    return "warning"

# error message
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# login
@app.route("/login", methods=["POST"])
def login():
    return form_login()

# logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/test')  
def test_index():  
    form = FormLogin()
    flash('flash-1')  
    flash('flash-2')  
    flash('welcome body')
    return render_template('index.html',form=form)      