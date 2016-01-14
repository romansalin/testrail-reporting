import logging
import os
import sys
from logging import handlers as log_handlers

from flask import Flask
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.cache import Cache
from flask.ext.restful import Api
from flask.ext.mongoengine import MongoEngine

from testrail_reporting import config
from testrail_reporting.auth.views import auth
from testrail_reporting.testrail.views import api_bp
from testrail_reporting.views import static_pages

log = logging.getLogger(__name__)

toolbar = DebugToolbarExtension()
cache = Cache()
api = Api()
db = MongoEngine()


def register_error_handler(app, code, page):
    app.register_error_handler(code,
                               lambda error: (render_template(page), code))


def setup_logging(app):
    if not app.debug:
        handler = log_handlers.RotatingFileHandler(
            app.config['LOGGING_LOCATION'],
            maxBytes=1024 * 1024 * 100,
            backupCount=20)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('iso8601').setLevel(logging.ERROR)


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(config.config[environment])
    config_filename = 'testrail_reporting.conf'
    app.config.from_pyfile('/etc/testrail_reporting/' + config_filename,
                           silent=True)
    app.config.from_pyfile(os.path.join(os.path.expanduser('~'),
                                        config_filename), silent=True)

    setup_logging(app)

    toolbar.init_app(app)
    cache.init_app(app, config=app.config['CACHING'])
    api.init_app(app)
    db.init_app(app)

    app.register_blueprint(static_pages, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    register_error_handler(app, 401, '401.html')
    register_error_handler(app, 404, '404.html')
    register_error_handler(app, 500, '500.html')

    return app
