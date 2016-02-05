from flask import Blueprint

from testrail_reporting.extensions import api
from testrail_reporting.resources import auth
from testrail_reporting.resources import errors
from testrail_reporting.resources import reports
from testrail_reporting.resources import testrail

api_bp = Blueprint('api', __name__)
api.init_app(api_bp)
