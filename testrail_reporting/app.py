#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import sys
from logging import handlers as log_handlers

from flask import Flask
from flask import render_template
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api

from testrail_reporting.auth.views import auth
from testrail_reporting.views import static_pages
from testrail_reporting.testrail.views import api_bp

log = logging.getLogger(__name__)

db = MongoEngine()


def register_error_handler(app, code, page):
    app.register_error_handler(code,
                               lambda error: (render_template(page), code))


def setup_logging(app):
    formatter = logging.Formatter(
        '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
    if not app.debug:
        handler = log_handlers.RotatingFileHandler(
            '/var/log/testrail_reporting/testrail_reporting.log',
            maxBytes=1024 * 1024 * 100,
            backupCount=20)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('iso8601').setLevel(logging.ERROR)


def create_app(config_object, enable_logging=True):
    app = Flask(__name__)
    api = Api(app)

    config_filename = 'testrail_reporting.conf'
    app.config.from_object(config_object)
    app.config.from_pyfile('/etc/testrail_reporting/' + config_filename,
                           silent=True)
    app.config.from_pyfile(os.path.join(os.path.expanduser('~') +
                                        config_filename), silent=True)

    if enable_logging:
        setup_logging(app)

    global db
    db.init_app(app)

    app.register_blueprint(static_pages, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    register_error_handler(app, 401, '401.html')
    register_error_handler(app, 404, '404.html')
    register_error_handler(app, 500, '500.html')

    return app
