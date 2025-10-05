from flask import Blueprint

# Import blueprints from submodules
from .customer import customer_bp
from .photographer import photographer_bp

# Auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import auth