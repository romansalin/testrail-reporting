from collections import Counter
from collections import OrderedDict
from datetime import datetime
from itertools import chain
import json
import logging
import os

from flask import current_app as app
import xlsxwriter

from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs, Reports)

log = logging.getLogger(__name__)


class ExcelReport(object):
    def __init__(self, filename):
        self.filename = filename

    def _calc_column_width(self, val):
        length = 8
        max_length = 60
        if isinstance(val, int):
            length += len(str(val))
        elif isinstance(val, str):
            length += len(val.encode('ascii', 'ignore'))
        return length if length < max_length else max_length

    def _build_worksheet(self, workbook, title, field_names, data):
        style_bold = workbook.add_format({'bold': True})
        worksheet = workbook.add_worksheet(title)
        for col, field in enumerate(field_names):
            width = self._calc_column_width(field)
            worksheet.set_column(col, col, width=width)
            worksheet.write(0, col, field, style_bold)
        worksheet.freeze_panes(1, 0)

        for row, record in enumerate(data, start=1):
            for col, field in enumerate(record):
                value = field
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, list):
                    value = json.dumps(value)
                width = self._calc_column_width(value)
                worksheet.set_column(col, col, width=width)
                worksheet.write(row, col, value)

    def build_workbook(self, workbook):
        raise NotImplementedError()

    def generate(self):
        log.info('Generating report...')
        filename = os.path.join(app.config['REPORTS_PATH'], self.filename)
        workbook = xlsxwriter.Workbook(filename)
        self.build_workbook(workbook)
        workbook.close()

        report = Reports(filename=self.filename)
        report.save()
        log.info('Report %s has been generated!', filename)
        return report


class MainReport(ExcelReport):
    def __init__(self, filename):
        super(MainReport, self).__init__(filename)

        # TODO(rsalin): getting cached data via API
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

        self.case_types = {
            d.pk: d.name
            for d in CaseTypes.objects.no_cache().only('id', 'name')}

        self.statuses = {
            d.pk: d.label
            for d in Statuses.objects.no_cache().only('id', 'label')}

    def _get_replaced_ids(self, row_data):
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
            elif k == 'type_id':
                additional_fields.update({'case_type': self.case_types.get(v)})
            elif k == 'status_id':
                additional_fields.update({'status': self.statuses.get(v)})
            elif k == 'created_by' or k == 'updated_by':
                additional_fields.update({k: self.users.get(v)})
        return additional_fields

    def _build_data_sheets(self, workbook):
        collections = [Users, CaseTypes, Statuses, Priorities, Projects,
                       Milestones, Plans, Configs, Suites, Cases, Sections,
                       Runs, Tests, Results]
        limit = 1000

        for collection in collections:
            field_names = collection.report_fields
            documents = collection.objects \
                .limit(limit) \
                .order_by('id') \
                .no_cache()
            data = []
            for document in documents:
                row_data = []
                row_data_map = OrderedDict(document.to_mongo())
                additional_rows = self._get_replaced_ids(row_data_map)
                row_data_map.update(additional_rows)
                for field in field_names:
                    value = row_data_map.get(field)
                    row_data.append(value)
                data.append(row_data)

            self._build_worksheet(workbook,
                                  collection.__name__,
                                  field_names,
                                  data)

    def _build_test_runs_sheet(self, workbook):
        field_names = ['QA team', 'Run ID', 'Run', 'Run Configuration',
                       'Milestone', 'Passed', 'ProdFailed', 'TestFailed',
                       'InfraFailed', 'Skipped', 'Other', 'Failed', 'Blocked',
                       'In progress', 'Fixed', 'Regression', 'Untested']

        case_teams = Cases.objects.only('id', 'custom_qa_team')
        case_teams_map = {}
        for case_team in case_teams:
            case_teams_map[case_team['id']] = getattr(case_team,
                                                      'custom_qa_team', None)

        run_tests = Tests.objects \
            .only('run_id', 'status_id', 'case_id') \
            .aggregate(
                {
                    "$group": {
                        "_id": {
                            "run_id": "$run_id",
                            "status_id": "$status_id",
                        },
                        "cases": {"$push": "$case_id"},
                        "count": {"$sum": 1},
                    },
                },
                {
                    "$group": {
                        "_id": "$_id.run_id",
                        "statuses": {
                            "$push": {
                                "status": "$_id.status_id",
                                "count": "$count",
                            }
                        },
                        "cases": {"$push": "$cases"},
                    }
                },
            )
        tests_map = {}
        for test in run_tests:
            statuses = {}
            for test_status in test['statuses']:
                statuses[self.statuses.get(
                    test_status['status'])] = test_status['count']

            teams = [case_teams_map.get(t) for t in
                     list(chain.from_iterable(test['cases']))
                     if case_teams_map.get(t) is not None]

            team = None
            try:
                team = Cases.teams[str(
                    Counter(teams).most_common(1)[0][0])]
            except IndexError:
                pass
            tests_map[test['_id']] = {
                'statuses': statuses,
                'team': team,
            }

        data = []
        runs = Runs.objects \
            .order_by('-id') \
            .only('id', 'name', 'config', 'milestone_id')
        for run in runs:
            run_id = run['id']
            if run_id in tests_map:
                data.append([
                    tests_map[run_id]['team'],
                    'R{0}'.format(run_id),
                    getattr(run, 'name', None),
                    getattr(run, 'config', None),
                    self.milestones.get(getattr(run, 'milestone_id', None)),
                    tests_map[run_id]['statuses'].get('Passed', 0),
                    tests_map[run_id]['statuses'].get('ProdFailed', 0),
                    tests_map[run_id]['statuses'].get('TestFailed', 0),
                    tests_map[run_id]['statuses'].get('InfraFailed', 0),
                    tests_map[run_id]['statuses'].get('Skipped', 0),
                    tests_map[run_id]['statuses'].get('Other', 0),
                    tests_map[run_id]['statuses'].get('Failed', 0),
                    tests_map[run_id]['statuses'].get('Blocked', 0),
                    tests_map[run_id]['statuses'].get('In progress', 0),
                    tests_map[run_id]['statuses'].get('Fixed', 0),
                    tests_map[run_id]['statuses'].get('Regression', 0),
                    tests_map[run_id]['statuses'].get('Untested', 0),
                ]),

        self._build_worksheet(workbook,
                              'Test Runs Report',
                              field_names,
                              data)

    def _build_test_automation_sheet(self, workbook):
        pass

    def build_workbook(self, workbook):
        self._build_data_sheets(workbook)
        self._build_test_runs_sheet(workbook)
        self._build_test_automation_sheet(workbook)
