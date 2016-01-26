import os

from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from flask import send_file

from testrail_reporting.auth.decorators import auth_required
from testrail_reporting.testrail.models import Reports

testrail = Blueprint('testrail', __name__)


@testrail.route('/reports/all')
@auth_required
def index():
    report = Reports.objects.order_by('-id').first()
    if not report:
        return jsonify({'error': 'Report not found'})

    filename = report.filename
    file_path = os.path.join(app.config['REPORTS_PATH'], filename)

    return send_file(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.'
                 'spreadsheetml.sheet',
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=0)
