from flask import Blueprint

# Import blueprints from submodules
from views.customer import customer_bp
from views.photographer import photographer_bp

# Auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from views import auth