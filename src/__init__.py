from flask import Flask

from logging.config import dictConfig

from .config import config_by_name, LOGGING_CONFIG
from .utils import db, flask_bcrypt
from .controller.hello import hello


def create_app(config_name):
    app = Flask('TravelNest')
    app.config.from_object(config_by_name[config_name])
    dictConfig(LOGGING_CONFIG)

    flask_bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(hello)

    return app
