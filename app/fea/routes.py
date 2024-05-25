from flask import render_template, jsonify
from . import fea
from .code import k_predict, abaqus_sumit


@fea.route('/', methods=["GET", "POST"])
def index():
    data = k_predict()
    return render_template("fea.html", form=data["form"], operation=data["operation"], properties=data["properties"], status=data["status"])

# run abaqus function
@fea.route("/run-abaqus", methods=["POST"])
def run_abaqus_api():
    data = abaqus_sumit()
    return jsonify(data)