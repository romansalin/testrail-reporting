from functools import wraps
import logging
import threading

import flask
from flask import g
from flask import session
import flask_oauthlib.client as oauth_client

from testrail_reporting import db

log = logging.getLogger(__name__)
auth = flask.Blueprint('auth', __name__)
oauth = oauth_client.OAuth()

_GOOGLE = None
_LOCK = threading.Lock()


def _create_remote_app():
    google = oauth.remote_app(
        'google',
        consumer_key=flask.current_app.config["GOOGLE_ID"],
        consumer_secret=flask.current_app.config["GOOGLE_SECRET"],
        request_token_params={
            'scope': 'https://www.googleapis.com/auth/userinfo.email',
            'hd': 'mirantis.com'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    google._tokengetter = get_access_token

    return google


def _get_google():
    global _GOOGLE, _LOCK

    if _GOOGLE is None:
        with _LOCK:
            if _GOOGLE is None:
                _GOOGLE = _create_remote_app()

    return _GOOGLE


def init_app(app):
    app.before_request(before_request)


def before_request():
    g.user = None
    if 'google_token' in session:
        g.user = db.find_user(google_token=session['google_token'])
        if not g.user:
            log.warning("User with google_token {0} "
                        "wasn't found in DB".format(session['google_token']))


@auth.route('/login')
def login():
    callback = flask.url_for('auth.authorized', _external=True)
    return _get_google().authorize(callback=callback)


@auth.route('/authorized')
def authorized():
    resp = _get_google().authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            flask.request.args['error_reason'],
            flask.request.args['error_description']
        )

    google_token = resp['access_token']
    session['google_token'] = (google_token, '')

    user_info = _get_google().get('userinfo').data
    user = db.find_user(email=user_info["email"])

    update = True
    if not user:
        user = user_info
        user["_id"] = user_info["email"]
        update = False

    user["google_token"] = google_token
    db.add_user(user, update=update)

    return flask.redirect(flask.url_for('about.show'))


def get_access_token():
    return session.get('google_token')


@auth.route('/logout')
def logout():
    session.pop('google_token', None)
    return flask.redirect(flask.url_for('login.show'))


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'google_token' not in session:
            log.debug("Unauthorized access. Throwing 401.")
            return flask.redirect(flask.url_for('login.show'))
        elif 'google_token' in session:
            google_token = session['google_token']
            user = db.find_user(google_token=google_token)
            if not user:
                log.warning("User with google_token {0} "
                            "wasn't found in DB".format(google_token))
                return flask.redirect(flask.url_for('login.show'))

        return f(*args, **kwargs)

    return decorated
