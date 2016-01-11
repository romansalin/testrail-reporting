from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Email


class DemoForm(Form):
    pass
