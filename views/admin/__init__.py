from flask import Blueprint

# Admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import dashboard
