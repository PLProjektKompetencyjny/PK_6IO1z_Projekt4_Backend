from flask import Flask

from logging.config import dictConfig

from .config import config_by_name, LOGGING_CONFIG
from src.controller.blueprint.database import database
from src.controller.blueprint.auth import auth
from src.controller.blueprint.invoice import invoice
from src.controller.blueprint.mailing import mailing
from .utils.utils import db, jwt

from src.service.scheduler.scheduler import setup_scheduler_for_payments

from flask_cors import CORS
import os


def create_app(config_name):
    app = Flask('TravelNest')
    app.config.from_object(config_by_name[config_name])

    dictConfig(LOGGING_CONFIG)
    db.init_app(app)

    app.register_blueprint(database)
    app.register_blueprint(auth)
    app.register_blueprint(invoice)
    app.register_blueprint(mailing)

    jwt.init_app(app)

    CORS(app)

    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        with app.app_context():
            setup_scheduler_for_payments(app)

    return app
