import logging

from flask.ext.security import RoleMixin
from flask.ext.security import UserMixin

from testrail_reporting.extensions import db

log = logging.getLogger(__name__)


class AuthRole(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __unicode__(self):
        return self.name


class AuthUser(db.DynamicDocument, UserMixin):
    id = db.StringField()
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    name = db.StringField()
    family_name = db.StringField()
    given_name = db.StringField()
    picture = db.StringField()
    hd = db.StringField()
    verified_email = db.BooleanField()
    google_token = db.StringField()
    roles = db.ListField(db.ReferenceField(AuthRole), default=[])

    @classmethod
    def get_current_user(cls, google_token):
        user = cls.objects(google_token=google_token)
        if not user:
            log.warning("User with google_token {0} "
                        "wasn't found in DB".format(google_token))
        return user

    def __unicode__(self):
        return '{0} {0} ({1})'.format(self.name, self.family_name, self.email)
