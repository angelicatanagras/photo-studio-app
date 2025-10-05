from flask import Flask


def create_app():
    app = Flask(__name__)
    app.debug = True

    from . import views
    app.register_blueprint(views.views, url_prefix='/')

    return app
