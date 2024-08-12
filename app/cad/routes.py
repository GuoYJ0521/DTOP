from flask import render_template, request
from flask_login import login_required, current_user
from . import cad
from .code import get_controller, post_controller
from .models import *

@cad.route("/")
@login_required
def index():
    return render_template("cad.html", user=current_user)

@cad.route("/controller/<int:id>", methods=["GET", "POST"])
def controller(id):
    if request.method == "GET":
        return get_controller(id)
    elif request.method == "POST":
        return post_controller(id)
