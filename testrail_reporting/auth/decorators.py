from functools import wraps
import logging

from flask import redirect
from flask import session
from flask import url_for

from testrail_reporting.auth import oauth
from testrail_reporting.auth.models import User

log = logging.getLogger(__name__)


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        google_token = session.get(oauth.GOOGLE_TOKEN)
        if not google_token:
            log.debug("Unauthorized access. Throwing 401.")
            return redirect(url_for('pages.login'))
        else:
            user = User.objects(google_token=google_token)
            if not user:
                log.warning("User with google_token {0} "
                            "wasn't found in DB".format(google_token))
                return redirect(url_for('pages.login'))

        return f(*args, **kwargs)

    return decorated
