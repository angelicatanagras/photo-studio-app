from flask import Blueprint

customer_bp = Blueprint('customer', __name__)

from views.customer import main
