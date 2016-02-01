import os

from flask import Blueprint
from flask import current_app as app
from flask import send_file

from testrail_reporting.auth.decorators import auth_required
from testrail_reporting.testrail.reports import MainReport
from testrail_reporting.utils import get_dt_iso

testrail = Blueprint('testrail', __name__)


@testrail.route('/reports/all')
@auth_required
def index():
    filename = 'testrail-report-{0}.xlsx'.format(get_dt_iso())
    report = MainReport(filename)
    report.generate()
    file_path = os.path.join(app.config['REPORTS_PATH'], filename)

    return send_file(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.'
                 'spreadsheetml.sheet',
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=0)
