import cStringIO
from datetime import datetime
import json
from collections import OrderedDict

import xlsxwriter

from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)


class MainReport(object):
    def __init__(self):
        # TODO(rsalin): move to model and cache for a while
        self.users = {
            d.pk: '{0} ({1})'.format(d.name, d.email)
            for d in Users.objects.no_cache().only('id', 'name', 'email')}

        self.projects = {
            d.pk: d.name
            for d in Projects.objects.no_cache().only('id', 'name')}

        self.milestones = {
            d.pk: d.name
            for d in Milestones.objects.no_cache().only('id', 'name')}

        self.suites = {
            d.pk: d.name
            for d in Suites.objects.no_cache().only('id', 'name')}

        self.priorities = {
            d.pk: d.name
            for d in Priorities.objects.no_cache().only('id', 'name')}

        self.sections = {
            d.pk: d.name
            for d in Sections.objects.no_cache().only('id', 'name')}

        self.case_types = {
            d.pk: d.name
            for d in CaseTypes.objects.no_cache().only('id', 'name')}

        self.plans = {
            d.pk: d.name
            for d in Plans.objects.no_cache().only('id', 'name')}

        self.status = {
            d.pk: d.label
            for d in Statuses.objects.no_cache().only('id', 'label')}

        self.cases = {
            d.pk: d.title
            for d in Cases.objects.no_cache().only('id', 'title')}

        self.runs = {
            d.pk: d.name
            for d in Runs.objects.no_cache().only('id', 'name')}

        self.tests = {
            d.pk: d.title
            for d in Tests.objects.no_cache().only('id', 'title')}

    def _calc_column_width(self, val):
        length = 8
        max_length = 60
        if isinstance(val, int):
            length += len(str(val))
        elif isinstance(val, basestring):
            length += len(val.encode('ascii', 'ignore'))

        return length if length < max_length else max_length

    def _get_row_data(self, document):
        data = document.to_mongo()
        fields = document.xlsx_fields

        for key in data:
            if key != '_id' and key not in fields:
                del data[key]

        for field in fields:
            if field not in data:
                data[field] = None

        return OrderedDict(data)

    def _replace_ids(self, row_data):
        additional_fields = OrderedDict()
        for k, v in row_data.items():
            if k == 'project_id':
                additional_fields.update({'project': self.projects.get(v)})
            elif k == 'milestone_id':
                additional_fields.update({'milestone': self.milestones.get(v)})
            elif k == 'assignedto_id':
                additional_fields.update({'assignedto': self.users.get(v)})
            elif k == 'suite_id':
                additional_fields.update({'suite': self.suites.get(v)})
            elif k == 'priority_id':
                additional_fields.update({'priority': self.priorities.get(v)})
            elif k == 'section_id':
                additional_fields.update({'section': self.sections.get(v)})
            elif k == 'type_id':
                additional_fields.update({'type': self.case_types.get(v)})
            elif k == 'plan_id':
                additional_fields.update({'plan': self.plans.get(v)})
            elif k == 'status_id':
                additional_fields.update({'status': self.status.get(v)})
            elif k == 'case_id':
                additional_fields.update({'case': self.cases.get(v)})
            elif k == 'run_id':
                additional_fields.update({'run': self.runs.get(v)})
            elif k == 'test_id':
                additional_fields.update({'test': self.tests.get(v)})

        row_data.update(additional_fields)
        return row_data

    def generate_xlsx(self):
        collections = [Users, CaseTypes, Statuses, Priorities, Projects,
                       Milestones, Plans, Configs, Suites, Cases, Sections,
                       Runs, Tests, Results]

        str_io = cStringIO.StringIO()
        workbook = xlsxwriter.Workbook(str_io)
        bold = workbook.add_format({'bold': True})

        for collection in collections:
            row = 1
            worksheet = workbook.add_worksheet(collection.__name__)
            for document in collection.objects.no_cache().order_by('id'):
                row_data = self._get_row_data(document)
                row_data = self._replace_ids(row_data)
                row_data = OrderedDict(sorted(row_data.items(),
                                              key=lambda x: x[0]))

                col = 0
                for k, v in row_data.items():
                    if row == 1:
                        width = self._calc_column_width(k)
                        worksheet.set_column(col, col, width=width)
                        worksheet.write(0, col, k, bold)

                    if isinstance(v, datetime):
                        v = v.isoformat()
                    elif isinstance(v, list):
                        v = json.dumps(v)

                    width = self._calc_column_width(v)
                    worksheet.set_column(col, col, width=width)
                    worksheet.write(row, col, v)

                    col += 1
                row += 1

        workbook.close()
        return str_io.getvalue()
