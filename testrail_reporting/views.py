from flask import Blueprint
from flask import render_template

from testrail_reporting.auth import views as auth_views

static_pages = Blueprint('static_pages', __name__)


@static_pages.route('/')
@auth_views.requires_auth
def show_index():
    return render_template('index.html')


@static_pages.route('/login')
def show_login():
    return render_template("auth/login.html")
