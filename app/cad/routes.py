from flask import render_template
from flask_login import login_required, current_user
from . import cad
from .code import get_controller

@cad.route("/")
@login_required
def index():
    return render_template("cad.html", user=current_user)

@cad.route("/controller/<int:id>")
def controller(id):
    return get_controller(id)