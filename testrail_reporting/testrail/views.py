import cStringIO

from flask import Blueprint
from flask import Response
import xlsxwriter

from testrail_reporting.auth.decorators import auth_required
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)

testrail = Blueprint('testrail', __name__)


def _generate_xlsx(filename):
    workbook = xlsxwriter.Workbook(filename)

    worksheet_users = workbook.add_worksheet('Users')
    for user in Users.objects:
        worksheet_users.write('A1', 'Hello world')

    worksheet_case_types = workbook.add_worksheet('Case Types')

    worksheet_statuses = workbook.add_worksheet('Statuses')

    worksheet_priorities = workbook.add_worksheet('Priorities')

    workbook.close()

    str_io = cStringIO.StringIO()

    return str_io.getvalue()


@testrail.route('/download-vghe32yfta98mwtv8oviyd3nqbfeq6dh')
# @auth_required
def index():
    filename = 'testrail.xlsx'
    xlsx = _generate_xlsx(filename)
    return Response(xlsx,
                    mimetype='application/vnd.openxmlformats-officedocument.'
                             'spreadsheetml.sheet',
                    headers={'Content-Disposition':
                             'attachment;filename={0}'.format(filename)})
