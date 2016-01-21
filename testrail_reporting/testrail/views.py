from flask import Blueprint
from flask import Response

from testrail_reporting.auth.decorators import auth_required

from testrail_reporting.testrail import reports

testrail = Blueprint('testrail', __name__)


@testrail.route('/reports/all')
# @auth_required
def index():
    filename = 'testrail-report.xlsx'
    report = reports.MainReport()
    xlsx = report.generate_xlsx()
    return Response(xlsx,
                    mimetype='application/vnd.openxmlformats-officedocument.'
                             'spreadsheetml.sheet',
                    headers={'Content-Disposition':
                             'attachment;filename={0}'.format(filename)})
