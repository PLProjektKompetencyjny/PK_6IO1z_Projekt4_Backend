from logging.config import dictConfig

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
            'filename': 'app.log',
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


def configure_logging():
    dictConfig(LOGGING_CONFIG)
