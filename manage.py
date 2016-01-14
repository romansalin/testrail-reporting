#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.script import Server

from testrail_reporting.app import create_app
from testrail_reporting.cmd.sync import Sync

manager = Manager(create_app)
manager.add_option('-e', '--environment',
                   dest='environment',
                   default='development',
                   help='config file',
                   required=False)

manager.add_command('runserver', Server(host='127.0.0.1', port=9000))
manager.add_command('sync', Sync())


if __name__ == '__main__':
    manager.run()
