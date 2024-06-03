from flask import Flask

from logging.config import dictConfig

from .config import config_by_name, LOGGING_CONFIG
from src.controller.blueprint.database import database
from src.controller.blueprint.auth import auth
from src.controller.blueprint.mailing import mailing
from .utils.utils import db, jwt

from flask_cors import CORS

def create_app(config_name):
    app = Flask('TravelNest')
    app.config.from_object(config_by_name[config_name])

    dictConfig(LOGGING_CONFIG)
    db.init_app(app)

    app.register_blueprint(database)
    app.register_blueprint(auth)
    app.register_blueprint(mailing)

    jwt.init_app(app)
    
    CORS(app)

    return app
