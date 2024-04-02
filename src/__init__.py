from flask import Flask, Blueprint

from logging.config import dictConfig

from .config import config_by_name, LOGGING_CONFIG
from .utils import db, flask_bcrypt
from .controller.hello import hello

mailing = Blueprint('mailing', __name__, url_prefix='/mailing')
def create_app(config_name):
    app = Flask('TravelNest')
    app.config.from_object(config_by_name[config_name])
    dictConfig(LOGGING_CONFIG)

    flask_bcrypt.init_app(app)
    db.init_app(app)


    app.register_blueprint(hello)
    app.register_blueprint(mailing)

    return app
