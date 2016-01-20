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


def _calc_column_width(val):
    length = 6
    if isinstance(val, int):
        length += len(str(val))
    elif isinstance(val, basestring):
        length += len(val.encode('ascii', 'ignore'))
    return length


def _get_xlsx_columns(document):
    data = document.to_mongo()
    fields = document.xlsx_fields

    for key in data:
        if key != '_id' and key not in fields:
            del data[key]

    for field in fields:
        if field not in data:
            data[field] = None

    return sorted(data.items(), key=lambda e: e[0])


def _generate_xlsx():
    collections = [Users, CaseTypes, Statuses, Priorities, Projects,
                   Milestones, Plans, Configs, Suites, Cases, Sections, Runs,
                   Tests, Results]

    str_io = cStringIO.StringIO()
    workbook = xlsxwriter.Workbook(str_io)
    bold = workbook.add_format({'bold': True})

    for collection in collections:
        row = 1
        worksheet = workbook.add_worksheet(collection.__name__)
        for document in collection.objects:
            col = 0
            data = _get_xlsx_columns(document)
            for k, v in data:
                width = _calc_column_width(v)

                if row == 1:
                    worksheet.set_column(0, 0, width=width)
                    worksheet.write(0, col, k, bold)

                if isinstance(v, list):
                    v = json.dumps(v)

                worksheet.set_column(col, col, width=width)
                worksheet.write(row, col, v)
                col += 1
            row += 1

    workbook.close()
    return str_io.getvalue()


@testrail.route('/download-vghe32yfta98mwtv8oviyd3nqbfeq6dh')
# @auth_required
def index():
    filename = 'testrail.xlsx'
    xlsx = _generate_xlsx()
    return Response(xlsx,
                    mimetype='application/vnd.openxmlformats-officedocument.'
                             'spreadsheetml.sheet',
                    headers={'Content-Disposition':
                             'attachment;filename={0}'.format(filename)})
