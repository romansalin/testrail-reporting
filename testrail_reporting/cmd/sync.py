from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.extensions import db


class Sync(Command):
    def run(self):
        app.logger.info('Run TestRail sync...')
