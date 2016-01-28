import logging

from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from testrail_reporting.auth.models import AuthUser
from testrail_reporting.auth.oauth import get_google

log = logging.getLogger(__name__)
auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    callback = url_for('auth.authorized', _external=True)
    return get_google().authorize(callback=callback)


@auth.route('/authorized')
def authorized():
    resp = get_google().authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'],
        )

    google_token = resp['access_token']
    session['google_token'] = (google_token, '')

    user_info = get_google().get('userinfo').data
    user_info.update({'google_token': google_token})
    AuthUser.objects(email=user_info["email"]).update_one(upsert=True,
                                                          **user_info)

    return redirect(url_for('pages.index'))


@auth.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('pages.login'))
