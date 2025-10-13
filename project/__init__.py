import os
import sys
from flask import Flask
from flask_mysqldb import MySQL

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mysql = MySQL()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'

    app = Flask(__name__)

    # Import config from parent directory
    from config import config
    app.config.from_object(config[config_name])

    # Initialize Flask-MySQLdb
    mysql.init_app(app)

    # Import views module to get inject_current_user function
    from .views import inject_current_user
    app.context_processor(inject_current_user)

    # Register blueprints
    from .views import customer_bp, photographer_bp, auth_bp, admin_bp
    app.register_blueprint(customer_bp)
    app.register_blueprint(photographer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
