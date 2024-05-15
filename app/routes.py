from flask import render_template, jsonify, url_for, redirect, flash
from app import app, mail, login
from app.dt_controller.resData import *
from flask_mail import Message
from flask_login import login_user, current_user, login_required, logout_user

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
    form = FormRegister()
    if request.method == 'POST':
        user = User(
            name = request.form['username'],
            email = request.form['email'],
            pwd = request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        form.username.data=''
        form.email.data=''

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
    msg_title = 'DT alert'
    #  寄件者，若參數有設置就不需再另外設置
    msg_sender = 'mailtrap@demomailtrap.com'
    #  收件者，格式為list，否則報錯
    msg_recipients = ['yijunguo473@gmail.com']
    #  郵件內容
    sensor = request.json.get('sensor')
    location = request.json.get('location')
    alert = request.json.get('alert')
    msg_body = f"異常-{location}{sensor}\n建議-{alert}"
    #  也可以使用html
    msg = Message(msg_title,
                  sender=msg_sender,
                  recipients=msg_recipients)
    msg.body = msg_body
    #  msg.html = msg_html
    
    #  mail.send:寄出郵件
    mail.send(msg)
    return 'send successfully'

# log infomation
@app.route("/log", methods=["POST"])
def log():
    # warning = request.json.get('id')
    sensor = request.json.get('sensor')
    location = request.json.get('location')
    alert = request.json.get('alert')
    warning = f"異常-{location}{sensor} 建議-{alert}"
    app.logger.warning(warning)
    return "warning"

# error message
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# login
@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    pwd = request.form['password']

    user = db.session.query(User).filter_by(email=email).first()
    if user:
        # check pawsseord
        if user.check_password(pwd):
            login_user(user, True)
            return redirect(url_for("index"))
        else:
            flash("Wrong Email or Password")
            return redirect(url_for("index"))
    else:
            flash("Wrong Email or Password")
            return redirect(url_for("index"))

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