import logging

from flask.ext.security import RoleMixin
from flask.ext.security import UserMixin

from testrail_reporting.extensions import db

log = logging.getLogger(__name__)


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.DynamicDocument,  UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    id = db.StringField()
    google_token = db.StringField()
    name = db.StringField()
    family_name = db.StringField()
    given_name = db.StringField()
    picture = db.StringField()
    hd = db.StringField()
    verified_email = db.BooleanField()

    @classmethod
    def get_current_user(cls, google_token):
        user = cls.objects(google_token=google_token)
        if not user:
            log.warning("User with google_token {0} "
                        "wasn't found in DB".format(google_token))
        return user
