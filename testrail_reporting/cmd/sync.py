import asyncio
import logging

from flask import current_app as app
from flask.ext.script import Command

from testrail_reporting.testrail import testrail_client
from testrail_reporting.testrail.models import (
    Users, Projects, Milestones, Plans, Suites, Runs, Sections, Cases, Tests,
    Results, CaseTypes, Statuses, Priorities, Configs, Syncs)

from testrail_reporting.utils import get_now

log = logging.getLogger(__name__)


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
            log.error(e.message)
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

    async def get_case_types(self):
        case_types = await self.get_data('case_types')
        self.clean_data(case_types, CaseTypes)
        for case_type in case_types:
            new_case_type = CaseTypes(**case_type)
            new_case_type.save()

    async def get_statuses(self):
        statuses = await self.get_data('statuses')
        self.clean_data(statuses, Statuses)
        for status in statuses:
            new_status = Statuses(**status)
            new_status.save()

    async def get_priorities(self):
        priorities = await self.get_data('priorities')
        self.clean_data(priorities, Priorities)
        for priority in priorities:
            new_priority = Priorities(**priority)
            new_priority.save()

    async def get_milestones(self, project):
        milestones = await self.get_data('milestones/{0}'.format(
            project['id']))
        for milestone in milestones:
            new_milestone = Milestones(**milestone)
            new_milestone.save()

    async def get_configs(self, project):
        configs = await self.get_data('configs/{0}'.format(project['id']))
        for config in configs:
            new_config = Configs(**config)
            new_config.save()

    async def get_sections(self, project, suite):
        sections = await self.get_data('sections/{0}&suite_id={1}'.format(
            project['id'], suite['id']))
        for section in sections:
            new_section = Sections(**section)
            new_section.save()

    async def get_cases(self, project, suite):
        cases = await self.get_data('cases/{0}&suite_id={1}'.format(
            project['id'], suite['id']))
        for case in cases:
            new_case = Cases(**case)
            new_case.save()

    async def get_suites(self, project):
        suites = await self.get_data('suites/{0}'.format(project['id']))
        for suite in suites:
            log.info('Sync Suite "{0}"'.format(suite.get('name')))
            new_suite = Suites(**suite)
            new_suite.save()

            await asyncio.wait([
                self.get_sections(project, suite),
                self.get_cases(project, suite),
            ])

    # TODO(rsalin): optimization
    async def get_plans(self, project):
        plan_runs = []
        plans = await self.get_data('plans/{0}'.format(project['id']))
        for plan in plans:
            log.info('Sync Plan "{0}"'.format(plan.get('name')))
            new_plan = Plans(**plan)
            new_plan.save()

            # repeat request to every plan because entries does't come
            # from plans/...
            plan_entries = await self.get_data(
                'plan/{0}'.format(plan['id']))
            for entry in plan_entries.get('entries', []):
                for run in entry['runs']:
                    run.update({
                        'config': entry.get('name'),
                        'suite_id': entry.get('suite_id'),
                    })
                    plan_runs.append(run)
        return plan_runs

    async def get_tests(self, run):
        tests = await self.get_data('tests/{0}'.format(run['id']))
        for test in tests:
            new_test = Tests(**test)
            new_test.save()

    async def get_results(self, run):
        results = await self.get_data(
            'results_for_run/{0}'.format(run['id']))
        for result in results:
            new_result = Results(**result)
            new_result.save()

    async def get_runs(self, project, plan_runs):
        runs = await self.get_data('runs/{0}'.format(project['id']))
        all_runs = plan_runs + runs
        for run in all_runs:
            log.info('Sync Run "{0}"'.format(run.get('name')))
            new_runs = Runs(**run)
            new_runs.save()

            await asyncio.wait([
                self.get_tests(run),
                self.get_results(run),
            ])

    async def get_projects(self):
        projects = await self.get_data('projects')
        self.clean_data(projects, Projects)
        for project in projects:
            log.info('Sync Project "{0}"'.format(project.get('name')))
            new_project = Projects(**project)
            new_project.save()

            await asyncio.wait([
                self.get_milestones(project),
                self.get_configs(project),
                self.get_suites(project),
            ])
            plan_runs = await self.get_plans(project)
            await self.get_runs(project, plan_runs)

    async def get_collections(self):
        await asyncio.wait([
            self.get_users(),
            self.get_case_types(),
            self.get_statuses(),
            self.get_priorities(),
            self.get_projects(),
        ])

    def run(self):
        log.info('Run TestRail sync...')
        Syncs(started=get_now()).save()

        self.client = testrail_client.TestRailClient(
            app.config['TESTRAIL_BASEURL'],
            app.config['TESTRAIL_USER'],
            app.config['TESTRAIL_PASSWORD'])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_collections())
        loop.close()

        Syncs.objects.order_by('-id').first().update(finished=get_now())
        log.info('TestRail sync has been finished!')
