from flask import Blueprint
from flask import render_template

from testrail_reporting.auth.decorators import auth_required

pages = Blueprint('pages', __name__, url_prefix='')


@pages.route('/')
@auth_required
def index():
    return render_template('index.html')


@pages.route('/login')
def login():
    return render_template('security/login_user.html')
