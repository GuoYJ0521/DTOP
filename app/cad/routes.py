from flask import render_template
from flask_login import login_required, current_user
from . import cad

@cad.route("/")
@login_required
def index():
    return render_template("cad.html", user=current_user)