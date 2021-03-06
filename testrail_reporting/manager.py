from flask.ext.script import Manager
from flask.ext.script import Server

from testrail_reporting.cmd.sync import Sync
from testrail_reporting import create_app

manager = Manager(create_app)

manager.add_option('-c', '--config',
                   dest='config_name',
                   default='development',
                   help='configuration (development, testing or production)',
                   required=False)

manager.add_command('runserver', Server(host='127.0.0.1'))
manager.add_command('sync', Sync())
