import os
from flask import Flask
from flask_mysqldb import MySQL
from config import config

mysql = MySQL()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mysql.init_app(app)

    # context processors
    from .views import inject_current_user
    app.context_processor(inject_current_user)

    # blueprints
    from .views import customer_bp, photographer_bp, auth_bp, admin_bp
    app.register_blueprint(customer_bp)
    app.register_blueprint(photographer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
