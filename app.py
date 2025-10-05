import os
from flask import Flask
from flask_mysqldb import MySQL
from .config import config
from .services.auth_service import inject_current_user

mysql = MySQL()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Flask-MySQLdb
    mysql.init_app(app)

    # Register context processor for current_user in templates
    app.context_processor(inject_current_user)

    # Register blueprints
    from .views import customer_bp, photographer_bp, auth_bp
    from .views.admin import admin_bp
    app.register_blueprint(customer_bp)
    app.register_blueprint(photographer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
