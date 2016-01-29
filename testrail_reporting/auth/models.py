import logging

from mongoengine import *

from flask.ext.security import RoleMixin
from flask.ext.security import UserMixin

log = logging.getLogger(__name__)


class AuthRole(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)

    def __str__(self):
        return self.name


class AuthUser(DynamicDocument, UserMixin):
    id = StringField()
    email = StringField(max_length=255)
    password = StringField(max_length=255)
    name = StringField()
    family_name = StringField()
    given_name = StringField()
    picture = StringField()
    hd = StringField()
    verified_email = BooleanField()
    google_token = StringField()
    roles = ListField(ReferenceField(AuthRole), default=[])

    @classmethod
    def get_current_user(cls, google_token):
        user = cls.objects(google_token=google_token)
        if not user:
            log.warning("User with google_token {0} "
                        "wasn't found in DB".format(google_token))
        return user

    def __str__(self):
        return '{0} {0} ({1})'.format(self.name, self.family_name, self.email)
