import logging
import os
import sys
from logging import handlers as log_handlers

from flask import Flask
from flask import render_template
from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.oauthlib.client import OAuth
from flask.ext.restful import Api
from flask.ext.security import MongoEngineUserDatastore
from flask.ext.security import Security

from testrail_reporting import config

log = logging.getLogger(__name__)

toolbar = DebugToolbarExtension()
oauth = OAuth()
cache = Cache()
api = Api()
db = MongoEngine()
security = Security()


def configure_app(app, environment):
    app.config.from_object(config.config[environment])
    config_filename = 'testrail_reporting.conf'
    app.config.from_pyfile('/etc/testrail_reporting/' + config_filename,
                           silent=True)
    app.config.from_pyfile(os.path.join(os.path.expanduser('~'),
                                        config_filename), silent=True)


def configure_logging(app):
    if not app.debug and not app.testing:
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


def configure_hook(app):

    @app.before_request
    def before_request():
        pass


def configure_extensions(app):
    db.init_app(app)
    cache.init_app(app, config=app.config['CACHING'])
    oauth.init_app(app)
    api.init_app(app)

    # Setup Flask-Security
    from testrail_reporting.auth import models as auth_models
    user_datastore = MongoEngineUserDatastore(db, auth_models.User,
                                              auth_models.Role)
    security.init_app(app, user_datastore)

    if app.debug:
        toolbar.init_app(app)


def configure_blueprints(app):
    from testrail_reporting.pages.views import pages
    app.register_blueprint(pages, url_prefix='/')

    from testrail_reporting.auth.views import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from testrail_reporting.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1.0')


def configure_template_filters(app):

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_error_handlers(app):
    def register_error_handler(code, page):
        app.register_error_handler(code, lambda error: (render_template(page),
                                                        code))

    register_error_handler(401, 'errors/401.html')
    register_error_handler(404, 'errors/404.html')
    register_error_handler(500, 'errors/500.html')


def configure_api_endpoints():
    pass


def create_app(environment='development'):
    app = Flask(__name__)

    configure_app(app, environment)
    configure_logging(app)
    configure_hook(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_api_endpoints()
    return app
