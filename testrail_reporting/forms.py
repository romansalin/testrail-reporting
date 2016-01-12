# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.mongoengine.wtf import model_form
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Email


class User(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)


class Content(db.EmbeddedDocument):
    text = db.StringField()
    lang = db.StringField(max_length=3)


class Post(db.Document):
    title = db.StringField(max_length=120, required=True, validators=[validators.InputRequired(message=u'Missing title.'),])
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.EmbeddedDocumentField(Content)

