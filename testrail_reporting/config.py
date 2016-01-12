# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


class Config(object):
    DEBUG = False
    TESTING = False

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = 'DPMhsEFQAfuXFd7xhXgjUjkYrwhZDC4e'

    # Secret key for signing cookies
    SECRET_KEY = 'dRvH46rb4tHG5TrSYGFDhLKnTeHdjCVB'

    MONGODB_SETTINGS = {'db': 'testrail'}

    GOOGLE_ID = 'FIXME'
    GOOGLE_SECRET = 'FIXME'


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': None,
        'host': 'localhost',
        'port': 27017,
        'username': None,
        'password': None,
    }


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
