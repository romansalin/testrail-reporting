import cStringIO

from flask import Blueprint
from flask import Response

from testrail_reporting.auth.decorators import auth_required
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configurations)

testrail = Blueprint('testrail', __name__)


def _generate_xlsx():

    str_io = cStringIO.StringIO()

    return str_io.getvalue()


@testrail.route('/download-vghe32yfta98mwtv8oviyd3nqbfeq6dh')
# @auth_required
def index():
    filename = 'testrail_data.xlsx'
    xlsx = _generate_xlsx()
    return Response(xlsx,
                    mimetype='application/vnd.openxmlformats-officedocument.'
                             'spreadsheetml.sheet',
                    headers={'Content-Disposition':
                             'attachment;filename={0}'.format(filename)})
