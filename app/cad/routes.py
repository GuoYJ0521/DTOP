from flask import render_template, request
from flask_login import login_required, current_user
from . import cad
from .code import get_controller, post_controller
from .models import *

@cad.route("/<machine>/<machine_id>")
@login_required
def index(machine, machine_id):
    if machine == "Grinder":
        return render_template("cad.html", user=current_user, machine=machine, machine_id=machine_id)

@cad.route("/controller/<int:id>")
def controller(id):
    return get_controller(id)
