from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.testrail import testrail_client
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)

from testrail_reporting.utils import timestamp_to_utc


# TODO(rsalin): threading, too slow!
# TODO(rsalin): retrieve only new data and clean non-existent
# TODO(rsalin): getting Case Fields and Result Fields
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
        new_configs = []
        new_suites = []
        new_cases = []
        new_sections = []
        new_plans = []
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

            plan_runs = []
            plans = self.get_data('plans/{0}'.format(project['id']))
            for plan in plans:
                app.logger.info('Sync plan "{0}"'.format(plan.get('name')))

                plan['completed_on'] = timestamp_to_utc(
                    plan['completed_on'])
                plan['created_on'] = timestamp_to_utc(plan['created_on'])
                new_plans.append(Plans(**plan))

                # repeat request to every plan because entries does't come
                # from plans/...
                plan_entries = self.get_data('plan/{0}'.format(
                    plan['id']))
                for entry in plan_entries['entries']:
                    for run in entry['runs']:
                        run.update({
                            'config': entry['name'],
                            'suite_id': entry['suite_id'],
                        })
                        plan_runs.append(run)

            runs = self.get_data('runs/{0}'.format(project['id']))
            all_runs = plan_runs + runs
            for run in all_runs:
                app.logger.info('Sync run "{0}"'.format(run.get('name')))

                run['completed_on'] = timestamp_to_utc(
                    run['completed_on'])
                run['created_on'] = timestamp_to_utc(run['created_on'])
                new_runs.append(Runs(**run))

                tests = self.get_data('tests/{0}'.format(run['id']))
                for test in tests:
                    new_tests.append(Tests(**test))

                results = self.get_data(
                    'results_for_run/{0}'.format(run['id']))
                for result in results:
                    result['created_on'] = timestamp_to_utc(
                        result['created_on'])
                    new_results.append(Results(**result))

        app.logger.info('Start saving objects.')

        Users.objects.delete()
        if new_users:
            Users.objects.insert(new_users)

        CaseTypes.objects.delete()
        if new_case_types:
            CaseTypes.objects.insert(new_case_types)

        Statuses.objects.delete()
        if new_statuses:
            Statuses.objects.insert(new_statuses)

        Priorities.objects.delete()
        if new_priorities:
            Priorities.objects.insert(new_priorities)

        Projects.objects.delete()
        if new_projects:
            Projects.objects.insert(new_projects)

        Milestones.objects.delete()
        if new_milestones:
            Milestones.objects.insert(new_milestones)

        Configs.objects.delete()
        if new_configs:
            Configs.objects.insert(new_configs)

        Suites.objects.delete()
        if new_suites:
            Suites.objects.insert(new_suites)

        Cases.objects.delete()
        if new_cases:
            Cases.objects.insert(new_cases)

        Sections.objects.delete()
        if new_sections:
            Sections.objects.insert(new_sections)

        Plans.objects.delete()
        if new_plans:
            Plans.objects.insert(new_plans)

        Runs.objects.delete()
        if new_runs:
            Runs.objects.insert(new_runs)

        Tests.objects.delete()
        if new_tests:
            Tests.objects.insert(new_tests)

        Results.objects.delete()
        if new_results:
            Results.objects.insert(new_results)

        app.logger.info('TestRail sync has been finished!')
