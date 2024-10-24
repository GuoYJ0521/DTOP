from flask import render_template, jsonify
from flask_login import login_required, current_user
from . import fea
from .code import k_predict, abaqus_sumit


@fea.route('/<machine>/<machine_id>', methods=["GET", "POST"])
@login_required
def index(machine, machine_id):
    data = k_predict()
    return render_template("fea.html", form=data["form"], operation=data["operation"], properties=data["properties"], status=data["status"], user=current_user, machine=machine, machine_id=machine_id)

# run abaqus function
@fea.route("/abaqus", methods=["POST"])
@login_required
def run_abaqus_api():
    data = abaqus_sumit()
    return jsonify(data)