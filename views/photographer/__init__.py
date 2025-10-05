from flask import Blueprint

photographer_bp = Blueprint('photographer', __name__, url_prefix='/photographer')

from views.photographer import dashboard
