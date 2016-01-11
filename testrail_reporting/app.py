#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from flask import Flask
from flask import render_template
from flask.ext.restful import Api

from testrail_reporting.views.api import api_bp
from testrail_reporting.views.pages import static_pages

logger = logging.getLogger('__name__')

app = Flask(__name__)
api = Api(app)

app.config.from_object('testrail_reporting.conf')

app.register_blueprint(static_pages)
app.register_blueprint(api_bp)


def register_error_handler(app, code, page):
    app.register_error_handler(code, lambda error: (render_template(page),
                                                    code))

register_error_handler(app, 401, "401.html")
register_error_handler(app, 404, "404.html")
register_error_handler(app, 500, "500.html")
