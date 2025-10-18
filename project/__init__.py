import os
from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config

mysql = MySQL()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mysql.init_app(app)

    from .views import inject_current_user
    app.context_processor(inject_current_user)

    from .views import customer_bp, photographer_bp, auth_bp, admin_bp
    app.register_blueprint(customer_bp)
    app.register_blueprint(photographer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="Not Found"), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html", title="Server Error"), 500

    return app
