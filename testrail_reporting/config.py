import logging
import os


class Config(object):
    DEBUG = False
    TESTING = False

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = 'hard to guess string'

    # Secret key for signing cookies
    SECRET_KEY = 'hard to guess string'

    # Logging
    LOGGING_FORMAT = '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.INFO

    # DB
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DB = 'testrail_reporting'

    # Caching
    CACHING = {'CACHE_TYPE': 'simple'}

    # Google OAuth2
    GOOGLE_ID = 'FIXME'
    GOOGLE_SECRET = 'FIXME'


class ProductionConfig(Config):
    LOGGING_LOCATION = '/var/log/testrail_reporting/testrail_reporting.log'


class DevelopmentConfig(Config):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

config = {
    'development': 'testrail_reporting.config.DevelopmentConfig',
    'production': 'testrail_reporting.config.ProductionConfig',
    'testing': 'testrail_reporting.config.TestingConfig',
}
