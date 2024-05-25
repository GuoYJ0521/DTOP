from flask import Blueprint

cad = Blueprint('cad', __name__, template_folder='templates')

from . import routes