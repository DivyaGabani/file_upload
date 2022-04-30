import logging
import os
from logging.config import dictConfig

import flask
from flask import request, current_app

# from app.logging_config.log_formatters import RequestFormatter
from app import config

log_con = flask.Blueprint('log_con', __name__)


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("csvlog")
    log.debug("CSV file upload Logger Message(first_request)")
    return response


@log_con.before_app_first_request
def configure_logging():
    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("csvlog")
    log.debug("CSV file upload Logger Message(first_request)")


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(process)d] %(remote_addr)s requested %(url)s'
                      '%(levelname)s in %(module)s: %(message)s'
        },
        'CSVFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '%(filename)s uploaded by : %(host)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler.myapp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'myapp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.csvlog': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'CSVFormatter',
            'filename': os.path.join(config.Config.LOG_DIR, 'csvlog.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myapp'],
            'level': 'INFO',
            'propagate': False
        },
        'csvlog': {  # if __name__ == '__main__'
            'handlers': ['file.handler.csvlog'],
            'level': 'DEBUG',
            'propagate': False
        },

    }
}
