import threading

from flask import current_app
from flask import session

from testrail_reporting.extensions import oauth

_GOOGLE = None
_LOCK = threading.Lock()


def get_access_token():
    return session.get('google_token')


def _create_remote_app():
    google = oauth.remote_app(
        'google',
        consumer_key=current_app.config['GOOGLE_KEY'],
        consumer_secret=current_app.config['GOOGLE_SECRET'],
        request_token_params={
            'scope': 'https://www.googleapis.com/auth/userinfo.email',
            'hd': 'mirantis.com',
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    google._tokengetter = get_access_token
    return google


def get_google():
    global _GOOGLE, _LOCK

    if _GOOGLE is None:
        with _LOCK:
            if _GOOGLE is None:
                _GOOGLE = _create_remote_app()
    return _GOOGLE
