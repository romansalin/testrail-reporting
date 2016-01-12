#!/usr/bin/env python
from testrail_reporting.app import create_app

app = create_app('lpreports.config.Production')
app.run(host='0.0.0.0', port=80)
