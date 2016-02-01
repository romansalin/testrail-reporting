import asyncio
from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.testrail import testrail_client
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs, Syncs)

from testrail_reporting.utils import get_now


# TODO(rsalin): threading or async (too slow!)
# TODO(rsalin): retrieve only new data and clean non-existent
class Sync(Command):
    def __init__(self):
        super(Sync, self).__init__()
        self.client = None

    async def get_data(self, resource):
        data = []
        try:
            data = await self.client.send_get('get_' + resource)
        except testrail_client.APIError as e:
            app.logger.error(e.message)
        return data

    def clean_data(self, data, collection):
        current_users_id = collection.objects.scalar('id')
        id_to_detele = list(set(current_users_id) - set(u['id'] for u in data))
        collection.objects.filter(id__in=id_to_detele).delete()

    async def get_users(self):
        users = await self.get_data('users')
        self.clean_data(users, Users)
        for user in users:
            new_user = Users(**user)
            new_user.save()

    # @asyncio.coroutine
    # def get_case_types(self):
    #     case_types = self.get_data('case_types')
    #     self.clean_data(case_types, CaseTypes)
    #     for case_type in case_types:
    #         new_case_type = CaseTypes(**case_type)
    #         new_case_type.save()
    #
    # @asyncio.coroutine
    # def get_statuses(self):
    #     statuses = self.get_data('statuses')
    #     self.clean_data(statuses, Statuses)
    #     for status in statuses:
    #         new_status = Statuses(**status)
    #         new_status.save()
    #
    # @asyncio.coroutine
    # def get_priorities(self):
    #     priorities = self.get_data('priorities')
    #     self.clean_data(priorities, Priorities)
    #     for priority in priorities:
    #         new_priority = Priorities(**priority)
    #         new_priority.save()

    async def init(self, loop):
        await self.get_users()

    def run(self):
        app.logger.info('Run TestRail sync...')
        Syncs(started=get_now()).save()

        self.client = testrail_client.TestRailClient(
            app.config['TESTRAIL_BASEURL'],
            app.config['TESTRAIL_USER'],
            app.config['TESTRAIL_PASSWORD'])

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.get_users())
        loop.run_until_complete(self.init)
        # app.logger.info('Pending tasks at exit: %s',
        #                 asyncio.Task.all_tasks(loop))
        loop.stop()
        loop.close()

        # projects = self.get_data('projects')
        # self.clean_data(projects, Projects)
        # for project in projects:
        #     app.logger.info('Sync Project "{0}"'.format(project.get('name')))
        #     new_project = Projects(**project)
        #     new_project.save()
        #
        #     milestones = self.get_data('milestones/{0}'.format(project['id']))
        #     for milestone in milestones:
        #         new_milestone = Milestones(**milestone)
        #         new_milestone.save()
        #
        #     configs = self.get_data('configs/{0}'.format(project['id']))
        #     for config in configs:
        #         new_config = Configs(**config)
        #         new_config.save()
        #
        #     suites = self.get_data('suites/{0}'.format(project['id']))
        #     for suite in suites:
        #         app.logger.info('Sync Suite "{0}"'.format(suite.get('name')))
        #         new_suite = Suites(**suite)
        #         new_suite.save()
        #
        #         sections = self.get_data('sections/{0}&suite_id={1}'.format(
        #             project['id'], suite['id']))
        #         for section in sections:
        #             new_section = Sections(**section)
        #             new_section.save()
        #
        #         cases = self.get_data('cases/{0}&suite_id={1}'.format(
        #             project['id'], suite['id']))
        #         for case in cases:
        #             new_case = Cases(**case)
        #             new_case.save()
        #
        #     plan_runs = []
        #     plans = self.get_data('plans/{0}'.format(project['id']))
        #     for plan in plans:
        #         app.logger.info('Sync Plan "{0}"'.format(plan.get('name')))
        #         new_plan = Plans(**plan)
        #         new_plan.save()
        #
        #         # repeat request to every plan because entries does't come
        #         # from plans/...
        #         plan_entries = self.get_data(
        #             'plan/{0}'.format(plan['id'])).get('entries', [])
        #         for entry in plan_entries:
        #             for run in entry['runs']:
        #                 run.update({
        #                     'config': entry.get('name'),
        #                     'suite_id': entry.get('suite_id'),
        #                 })
        #                 plan_runs.append(run)
        #
        #     runs = self.get_data('runs/{0}'.format(project['id']))
        #     all_runs = plan_runs + runs
        #     for run in all_runs:
        #         app.logger.info('Sync Run "{0}"'.format(run.get('name')))
        #         new_runs = Runs(**run)
        #         new_runs.save()
        #
        #         tests = self.get_data('tests/{0}'.format(run['id']))
        #         for test in tests:
        #             new_test = Tests(**test)
        #             new_test.save()
        #
        #         results = self.get_data(
        #             'results_for_run/{0}'.format(run['id']))
        #         for result in results:
        #             new_result = Results(**result)
        #             new_result.save()

        Syncs.objects.order_by('-id').first().update(finished=get_now())
        app.logger.info('TestRail sync has been finished!')
