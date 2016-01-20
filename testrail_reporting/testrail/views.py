import cStringIO
import json

from flask import Blueprint
from flask import Response
import xlsxwriter

from testrail_reporting.auth.decorators import auth_required
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)

testrail = Blueprint('testrail', __name__)


def _calc_column_width(col, val):
    return '{0}:{0}'.format(chr(col + ord('A')), len(str(val)) + 2)


def _generate_xlsx(filename):
    objects = [Users, CaseTypes, Statuses, Priorities, Projects, Milestones,
               Plans, Configs, Suites, Cases, Sections, Runs, Tests, Results]

    str_io = cStringIO.StringIO()
    workbook = xlsxwriter.Workbook(str_io)
    bold = workbook.add_format({'bold': True})

    for obj in objects:
        row = 1
        worksheet = workbook.add_worksheet(obj.__name__)
        for record in obj.objects:
            col = 0
            record_items = sorted(record.to_mongo().items(),
                                  key=lambda e: e[0])
            for k, v in record_items:
                width = _calc_column_width(col, v)
                worksheet.set_column(width)

                if row == 1:
                    worksheet.write(0, col, k, bold)

                if isinstance(v, list):
                    v = json.dumps(v)

                worksheet.write(row, col, v)
                col += 1
            row += 1

    workbook.close()
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
