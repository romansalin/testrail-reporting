#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from flask.ext.script import Manager, Server

from testrail_reporting import app

log = logging.getLogger(__name__)

manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=5000,
                                        use_debugger=True))


def _create_app(conf='lpreports.config.Production'):
    return app.create_app(conf, enable_logging=False)


# @manager.command
# @click.option('--port', type=int, default=1111)
# @click.option('--host', default='127.0.0.1')
# def devserver(port, host):
#     app = _create_app('lpreports.config.Testing')
#     app.run(host=host, port=port)


@manager.command
def sync_testrail():
    app = _create_app()
    # with app.app_context():
    #     syncdb.syncdb()


if __name__ == '__main__':
    manager.run()
