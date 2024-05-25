from flask import Blueprint

fea = Blueprint('fea', __name__, template_folder='templates')

from . import routes