from functools import wraps
import logging

from flask import redirect
from flask import session
from flask import url_for

from testrail_reporting.auth.models import AuthUser

log = logging.getLogger(__name__)


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        google_token = session.get('google_token')
        if not google_token:
            log.debug("Unauthorized access.")
            return redirect(url_for('pages.login'))

        try:
            AuthUser.objects.get(google_token=google_token[0])
        except AuthUser.DoesNotExist:
            log.warning("User with google_token {0} "
                        "wasn't found in DB".format(google_token[0]))
            return redirect(url_for('pages.login'))

        return f(*args, **kwargs)
    return decorated
