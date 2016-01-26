from flask import Blueprint
from flask import Response

from testrail_reporting.auth.decorators import auth_required

from testrail_reporting.testrail import reports
from testrail_reporting.utils import get_dt_iso

testrail = Blueprint('testrail', __name__)


@testrail.route('/reports/all')
@auth_required
def index():
    filename = 'testrail-report-{0}.xlsx'.format(get_dt_iso())
    report = reports.MainReport()
    xlsx = report.generate_xlsx()
    return Response(xlsx,
                    mimetype='application/vnd.openxmlformats-officedocument.'
                             'spreadsheetml.sheet',
                    headers={'Content-Disposition':
                             'attachment;filename={0}'.format(filename)})
