from os import getenv

ADDRESS = getenv('DB_Address', 'localhost')
PORT = getenv('DB_Port', '5432')
DB_NAME = getenv('DB_Name', 'TravelNest')
USERNAME = getenv('DB_Username', 'tn_api_write')
PASSWORD = getenv('DB_Password', 'cba')

postgres_local_base = f"postgresql://{USERNAME}:{PASSWORD}@{ADDRESS}:{PORT}/{DB_NAME}"


class Config:
    SECRET_KEY = getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
)

key = Config.SECRET_KEY

LOGGING_CONFIG = {
    'version': 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(module)s] - [%(levelname)s] : %(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/flask-app/app.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    },
}
