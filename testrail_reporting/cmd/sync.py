from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.testrail import testrail_client
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)

from testrail_reporting.utils import timestamp_to_utc


# TODO(rsalin): threading, too slow!
# TODO(rsalin): retrieve only new data and clean non-existent
class Sync(Command):
    def __init__(self):
        super(Sync, self).__init__()
        self.client = None

    def get_data(self, resource):
        data = []
        try:
            data = self.client.send_get('get_' + resource)
        except testrail_client.APIError as e:
            app.logger.error(e.message)
        return data

    def run(self):
        app.logger.info('Run TestRail sync...')

        self.client = testrail_client.TestRailClient(
            app.config['TESTRAIL_BASEURL'],
            app.config['TESTRAIL_USER'],
            app.config['TESTRAIL_PASSWORD'])

        new_users = []
        new_case_types = []
        new_statuses = []
        new_priorities = []
        new_projects = []
        new_milestones = []
        new_plans = []
        new_configs = []
        new_suites = []
        new_cases = []
        new_sections = []
        new_runs = []
        new_tests = []
        new_results = []

        users = self.get_data('users')
        for user in users:
            new_users.append(Users(**user))

        case_types = self.get_data('case_types')
        for case_type in case_types:
            new_case_types.append(CaseTypes(**case_type))

        statuses = self.get_data('statuses')
        for status in statuses:
            new_statuses.append(Statuses(**status))

        priorities = self.get_data('priorities')
        for priority in priorities:
            new_priorities.append(Priorities(**priority))

        projects = self.get_data('projects')
        for project in projects:
            app.logger.info('Sync project "{0}"'.format(project.get('name')))
            project['completed_on'] = timestamp_to_utc(
                project['completed_on'])
            new_projects.append(Projects(**project))

            milestones = self.get_data('milestones/{0}'.format(project['id']))
            for milestone in milestones:
                milestone['completed_on'] = timestamp_to_utc(
                    project['completed_on'])
                milestone['due_on'] = timestamp_to_utc(
                    milestone['due_on'])
                new_milestones.append(Milestones(**milestone))

            plans = self.get_data('plans/{0}'.format(project['id']))
            for plan in plans:
                plan['completed_on'] = timestamp_to_utc(
                    plan['completed_on'])
                plan['created_on'] = timestamp_to_utc(plan['created_on'])
                new_plans.append(Plans(**plan))

            configs = self.get_data('configs/{0}'.format(project['id']))
            for config in configs:
                new_configs.append(Configs(**config))

            suites = self.get_data('suites/{0}'.format(project['id']))
            for suite in suites:
                app.logger.info('Sync suite "{0}"'.format(suite.get('name')))

                suite['completed_on'] = timestamp_to_utc(
                    suite['completed_on'])
                new_suites.append(Suites(**suite))

                cases = self.get_data('cases/{0}&suite_id={1}'.format(
                    project['id'], suite['id']))
                for case in cases:
                    case['created_on'] = timestamp_to_utc(
                        case['created_on'])
                    case['updated_on'] = timestamp_to_utc(
                        case['updated_on'])
                    new_cases.append(Cases(**case))

                sections = self.get_data('sections/{0}&suite_id={1}'.format(
                    project['id'], suite['id']))
                for section in sections:
                    new_sections.append(Sections(**section))

            runs = self.get_data('runs/{0}'.format(project['id']))
            for run in runs:
                app.logger.info('Sync run "{0}"'.format(run.get('name')))

                run['completed_on'] = timestamp_to_utc(
                    run['completed_on'])
                run['created_on'] = timestamp_to_utc(run['created_on'])
                new_runs.append(Runs(**run))

                tests = self.get_data('tests/{0}'.format(run['id']))
                for test in tests:
                    new_tests.append(Tests(**test))

                    results = self.get_data('results/{0}'.format(test['id']))
                    for result in results:
                        result['created_on'] = timestamp_to_utc(
                            result['created_on'])
                        new_results.append(Results(**result))

        app.logger.info('Start saving objects.')

        Users.objects.delete()
        Users.objects.insert(new_users)

        CaseTypes.objects.delete()
        CaseTypes.objects.insert(new_case_types)

        Statuses.objects.delete()
        Statuses.objects.insert(new_statuses)

        Priorities.objects.delete()
        Priorities.objects.insert(new_priorities)

        Projects.objects.delete()
        Projects.objects.insert(new_projects)

        Milestones.objects.delete()
        Milestones.objects.insert(new_milestones)

        Plans.objects.delete()
        Plans.objects.insert(new_plans)

        Configs.objects.delete()
        Configs.objects.insert(new_configs)

        Suites.objects.delete()
        Suites.objects.insert(new_suites)

        Cases.objects.delete()
        Cases.objects.insert(new_cases)

        Sections.objects.delete()
        Sections.objects.insert(new_sections)

        Runs.objects.delete()
        Runs.objects.insert(new_runs)

        Tests.objects.delete()
        Tests.objects.insert(new_tests)

        Results.objects.delete()
        Results.objects.insert(new_results)

        app.logger.info('TestRail sync has been finished!')
