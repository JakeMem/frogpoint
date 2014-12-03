#!/usr/bin/env python
import sys

sys.path.append('..')

from flask_script import Server, Manager, Shell
from parse_rest.connection import register

from frogpoint.app import app
from frogpoint.models import Merchant, Beacon, Coupon


def shell_context():
    register(app.config['PARSE_APPLICATION_ID'],
             app.config['PARSE_REST_API_KEY'])
    return {
        'app': app,
        'Merchant': Merchant,
        'Beacon': Beacon,
        'Coupon': Coupon,
    }

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=shell_context))


if __name__ == '__main__':
    manager.run()
