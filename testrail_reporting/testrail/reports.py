from collections import Counter, OrderedDict
from datetime import datetime
from itertools import chain
import json
import os

from flask import current_app as app
import xlsxwriter

from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs, Reports)


class ExcelReport(object):
    def __init__(self, filename):
        self.filename = filename

    def calc_column_width(self, val):
        length = 8
        max_length = 60
        if isinstance(val, int):
            length += len(str(val))
        elif isinstance(val, basestring):
            length += len(val.encode('ascii', 'ignore'))
        return length if length < max_length else max_length

    def populate(self, workbook):
        raise NotImplementedError()

    def generate(self):
        filename = os.path.join(app.config['REPORTS_PATH'], self.filename)
        workbook = xlsxwriter.Workbook(filename)
        self.populate(workbook)
        workbook.close()
        report = Reports(filename=self.filename)
        report.save()


class MainReport(ExcelReport):
    def __init__(self, filename):
        super(MainReport, self).__init__(filename)

        # TODO(rsalin): move to the model and cache for a while
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

        self.statuses = {
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

    def get_replaced_ids(self, row_data):
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
                additional_fields.update({'case_type': self.case_types.get(v)})
            elif k == 'plan_id':
                additional_fields.update({'plan': self.plans.get(v)})
            elif k == 'status_id':
                additional_fields.update({'status': self.statuses.get(v)})
            elif k == 'case_id':
                additional_fields.update({'case': self.cases.get(v)})
            elif k == 'run_id':
                additional_fields.update({'run': self.runs.get(v)})
            elif k == 'test_id':
                additional_fields.update({'test': self.tests.get(v)})
            elif k == 'created_by' or k == 'updated_by':
                additional_fields.update({k: self.users.get(v)})
        return additional_fields

    def populate(self, workbook):
        # TODO(romansalin): refactor to get DRY
        collections = [Users, CaseTypes, Statuses, Priorities, Projects,
                       Milestones, Plans, Configs, Suites, Cases, Sections,
                       Runs, Tests, Results]
        limit = 2000
        style_bold = workbook.add_format({'bold': True})

        for collection in collections:
            worksheet = workbook.add_worksheet(collection.__name__)
            report_fields = collection.report_fields

            for col, field in enumerate(report_fields):
                width = self.calc_column_width(field)
                worksheet.set_column(col, col, width=width)
                worksheet.write(0, col, field, style_bold)
            worksheet.freeze_panes(1, 0)

            documents = collection.objects \
                .limit(limit) \
                .order_by('id') \
                .no_cache()
            for row, document in enumerate(documents, start=1):
                row_data = OrderedDict(document.to_mongo())
                additional_rows = self.get_replaced_ids(row_data)
                row_data.update(additional_rows)

                for col, field in enumerate(report_fields):
                    value = row_data.get(field)
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    elif isinstance(value, list):
                        value = json.dumps(value)

                    width = self.calc_column_width(value)
                    worksheet.set_column(col, col, width=width)
                    worksheet.write(row, col, value)

        # Test runs report
        worksheet = workbook.add_worksheet('Test Runs Report')
        column_names = ['QA team', 'Run ID', 'Run', 'Run Configuration',
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
                    tests_map[run_id]['statuses'].get('Passed'),
                    tests_map[run_id]['statuses'].get('ProdFailed'),
                    tests_map[run_id]['statuses'].get('TestFailed'),
                    tests_map[run_id]['statuses'].get('InfraFailed'),
                    tests_map[run_id]['statuses'].get('Skipped'),
                    tests_map[run_id]['statuses'].get('Other'),
                    tests_map[run_id]['statuses'].get('Failed'),
                    tests_map[run_id]['statuses'].get('Blocked'),
                    tests_map[run_id]['statuses'].get('In progress'),
                    tests_map[run_id]['statuses'].get('Fixed'),
                    tests_map[run_id]['statuses'].get('Regression'),
                    tests_map[run_id]['statuses'].get('Untested'),
                ]),

        for col, field in enumerate(column_names):
            width = self.calc_column_width(field)
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

                width = self.calc_column_width(value)
                worksheet.set_column(col, col, width=width)
                worksheet.write(row, col, value)
