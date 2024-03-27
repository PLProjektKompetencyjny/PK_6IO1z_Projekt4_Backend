from flask import Flask

from logging.config import dictConfig

from .config import config_by_name, LOGGING_CONFIG
from .controller.database import test_database
from .utils.utils import db


def create_app(config_name):
    app = Flask('TravelNest')
    app.config.from_object(config_by_name[config_name])

    dictConfig(LOGGING_CONFIG)
    db.init_app(app)

    app.register_blueprint(test_database)

    return app
