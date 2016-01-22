from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.testrail import testrail_client
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs)

from testrail_reporting.utils import timestamp_to_utc


# TODO(rsalin): multithreading, too slow!
# TODO(rsalin): select from last data changes
# TODO(rsalin): clean non-existent data
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

        users = self.get_data('users')
        for user in users:
            u = Users(**user)
            u.save()

        case_types = self.get_data('case_types')
        for case_type in case_types:
            ct = CaseTypes(**case_type)
            ct.save()

        statuses = self.get_data('statuses')
        for status in statuses:
            st = Statuses(**status)
            st.save()

        priorities = self.get_data('priorities')
        for priority in priorities:
            pr = Priorities(**priority)
            pr.save()

        projects = self.get_data('projects')
        for project in projects:
            app.logger.info('Sync project "{0}"'.format(project.get('name')))

            project['completed_on'] = timestamp_to_utc(
                project['completed_on'])

            p = Projects(**project)
            p.save()

            milestones = self.get_data('milestones/{0}'.format(project['id']))
            for milestone in milestones:
                milestone['completed_on'] = timestamp_to_utc(
                    project['completed_on'])
                milestone['due_on'] = timestamp_to_utc(
                    milestone['due_on'])

                m = Milestones(**milestone)
                m.save()

            plans = self.get_data('plans/{0}'.format(project['id']))
            for plan in plans:
                plan['completed_on'] = timestamp_to_utc(
                    plan['completed_on'])
                plan['created_on'] = timestamp_to_utc(plan['created_on'])

                p = Plans(**plan)
                p.save()

            configs = self.get_data('configs/{0}'.format(project['id']))
            for config in configs:
                cfg = Configs(**config)
                cfg.save()

            suites = self.get_data('suites/{0}'.format(project['id']))
            for suite in suites:
                app.logger.info('Sync suite "{0}"'.format(suite.get('name')))

                suite['completed_on'] = timestamp_to_utc(
                    suite['completed_on'])

                s = Suites(**suite)
                s.save()

                cases = self.get_data('cases/{0}&suite_id={1}'.format(
                    project['id'], suite['id']))
                for case in cases:
                    case['created_on'] = timestamp_to_utc(
                        case['created_on'])
                    case['updated_on'] = timestamp_to_utc(
                        case['updated_on'])

                    c = Cases(**case)
                    c.save()

                sections = self.get_data('sections/{0}&suite_id={1}'.format(
                    project['id'], suite['id']))
                for section in sections:
                    sect = Sections(**section)
                    sect.save()

            runs = self.get_data('runs/{0}'.format(project['id']))
            for run in runs:
                app.logger.info('Sync run "{0}"'.format(run.get('name')))

                run['completed_on'] = timestamp_to_utc(
                    run['completed_on'])
                run['created_on'] = timestamp_to_utc(run['created_on'])

                r = Runs(**run)
                r.save()

                tests = self.get_data('tests/{0}'.format(run['id']))
                for test in tests:
                    r = Tests(**test)
                    r.save()

                    results = self.get_data('results/{0}'.format(test['id']))
                    for result in results:
                        result['created_on'] = timestamp_to_utc(
                            result['created_on'])

                        r = Results(**result)
                        r.save()

        app.logger.info('TestRail sync has been finished!')
