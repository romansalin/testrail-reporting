from datetime import datetime

from testrail_reporting.auth.models import AuthUser
from testrail_reporting.extensions import db

from testrail_reporting.utils import get_dt_iso
from testrail_reporting.utils import timestamp_to_utc


class TestRailBaseDocument(db.DynamicDocument):
    id = db.IntField(primary_key=True)

    meta = {
        'abstract': True,
    }


class Users(TestRailBaseDocument):
    report_fields = [
        '_id',
        'email',
        'is_active',
        'name',
    ]


class CaseTypes(TestRailBaseDocument):
    report_fields = [
        '_id',
        'is_default',
        'name',
    ]


class Priorities(TestRailBaseDocument):
    report_fields = [
        '_id',
        'is_default',
        'name',
        'priority',
        'short_name',
    ]


class Statuses(TestRailBaseDocument):
    report_fields = [
        '_id',
        'is_final',
        'is_system',
        'is_untested',
        'label',
        'name',
    ]


class Projects(TestRailBaseDocument):
    report_fields = [
        '_id',
        'announcement',
        'completed_on',
        'is_completed',
        'name',
        'show_announcement',
        'suite_mode',
        'url',
    ]

    completed_on = db.DateTimeField()

    def clean(self):
        if not isinstance(self.completed_on, datetime):
            self.completed_on = timestamp_to_utc(self.completed_on)


class Milestones(TestRailBaseDocument):
    report_fields = [
        '_id',
        'completed_on',
        'description',
        'due_on',
        'is_completed',
        'name',
        'project',
        'url',
    ]

    project_id = db.IntField(required=True, null=True)
    completed_on = db.DateTimeField()
    due_on = db.DateTimeField()

    def clean(self):
        if self.completed_on:
            self.completed_on = timestamp_to_utc(self.completed_on)
        if self.due_on:
            self.due_on = timestamp_to_utc(self.due_on)


class Plans(TestRailBaseDocument):
    report_fields = [
        '_id',
        'assignedto',
        'blocked_count',
        'completed_on',
        'created_by',
        'created_on',
        # TODO make it dynamic (regexp?)
        'custom_status1_count',
        'custom_status2_count',
        'custom_status3_count',
        'custom_status4_count',
        'custom_status5_count',
        'custom_status6_count',
        'custom_status7_count',
        'description',
        'failed_count',
        'is_completed',
        'milestone',
        'name',
        'passed_count',
        'project',
        'retest_count',
        'untested_count',
        'url',
    ]

    assignedto_id = db.IntField(null=True)
    created_by = db.IntField(null=True)
    milestone_id = db.IntField(required=True, null=True)
    project_id = db.IntField(required=True, null=True)


class Configs(TestRailBaseDocument):
    report_fields = [
        '_id',
        'configs',
        'name',
        'project',
    ]

    project_id = db.IntField(required=True, null=True)


class Suites(TestRailBaseDocument):
    report_fields = [
        '_id',
        'completed_on',
        'description',
        'is_baseline',
        'is_completed',
        'is_master',
        'name',
        'project',
        'url',
    ]

    project_id = db.IntField(required=True, null=True)


class Sections(TestRailBaseDocument):
    report_fields = [
        '_id',
        'depth',
        'description',
        'display_order',
        'parent_id',
        'name',
        'suite_id',
        'suite',
    ]

    suite_id = db.IntField(required=True, null=True)


class Cases(TestRailBaseDocument):
    report_fields = [
        '_id',
        'created_by',
        'created_on',
        'estimate',
        'estimate_forecast',
        'milestone',
        'priority',
        'refs',
        'section_id',
        'section',
        'suite_id',
        'suite',
        'title',
        'case_type',
        'updated_by',
        'updated_on',
        # Custom fields
        # TODO(rsalin): get this from get_case_fields
        'custom_case_complexity',
        'custom_qa_team',
        'custom_report_label',
        'custom_test_case_description',
        'custom_test_case_steps',
        'custom_test_group',
    ]

    # TODO(rsalin): get this from get_case_fields
    teams = {
        '1': 'Framework-CI',
        '2': 'Fuel',
        '3': 'Maintenance',
        '4': 'MOS',
        '5': 'Performance',
        '6': 'PCE',
        '7': 'Telco',
    }

    created_by = db.IntField(null=True)
    milestone_id = db.IntField(null=True)
    priority_id = db.IntField(required=True, null=True)
    section_id = db.IntField(required=True, null=True)
    suite_id = db.IntField(required=True, null=True)
    type_id = db.IntField(required=True, null=True)
    updated_by = db.IntField(required=True, null=True)


class Runs(TestRailBaseDocument):
    report_fields = [
        '_id',
        'assignedto',
        'blocked_count',
        'completed_on',
        'config',
        'config_ids',
        'created_by',
        'created_on',
        'custom_status1_count',
        'custom_status2_count',
        'custom_status3_count',
        'custom_status4_count',
        'custom_status5_count',
        'custom_status6_count',
        'custom_status7_count',
        'description',
        'failed_count',
        'include_all',
        'is_completed',
        'milestone',
        'plan_id',
        'plan',
        'name',
        'passed_count',
        'project',
        'retest_count',
        'suite_id',
        'suite',
        'untested_count',
        'url',
    ]

    assignedto_id = db.IntField(null=True)
    config = db.StringField(required=True, null=True)
    created_by = db.IntField(null=True)
    milestone_id = db.IntField(required=True, null=True)
    plan_id = db.IntField(required=True, null=True)
    project_id = db.IntField(required=True, null=True)
    suite_id = db.IntField(required=True, null=True)
    custom_qa_team = db.StringField(null=True)


class Tests(TestRailBaseDocument):
    report_fields = [
        '_id',
        'assignedto_id',
        'case_id',
        'case',
        'estimate',
        'estimate_forecast',
        'milestone',
        'priority',
        'refs',
        'run_id',
        'run',
        'status',
        'title',
        'case_type',
    ]

    assignedto_id = db.IntField(null=True)
    case_id = db.IntField(required=True, null=True)
    milestone_id = db.IntField(required=True, null=True)
    priority_id = db.IntField(required=True, null=True)
    run_id = db.IntField(required=True, null=True)
    type_id = db.IntField(required=True, null=True)


class Results(TestRailBaseDocument):
    report_fields = [
        '_id',
        'assignedto',
        'comment',
        'created_by',
        'created_on',
        'defects',
        'elapsed',
        'status',
        'test_id',
        'test',
        'version',
    ]

    assignedto_id = db.IntField(null=True)
    created_by = db.IntField(null=True)
    test_id = db.IntField(required=True, null=True)


class Syncs(db.Document):
    started = db.DateTimeField(required=True)
    finished = db.DateTimeField()

    def __unicode__(self):
        return '{0} - {1}'.format(get_dt_iso(self.started),
                                  get_dt_iso(self.finished) or '...')


class Reports(db.Document):
    added = db.DateTimeField(default=datetime.now)
    modified = db.DateTimeField()
    filename = db.StringField(required=True)
    created_by = db.ReferenceField(AuthUser)

    def __unicode__(self):
        return self.filename

    def save(self, **kwargs):
        self.modified = datetime.now()
        super(Reports, self).save(**kwargs)
