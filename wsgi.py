#!/usr/bin/env python
from testrail_reporting import create_app

app = create_app('production')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
