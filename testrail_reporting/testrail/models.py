from datetime import datetime

from mongoengine import *

from testrail_reporting.auth.models import AuthUser
from testrail_reporting.utils import get_dt_iso
from testrail_reporting.utils import timestamp_to_utc


class TestRailDocument(DynamicDocument):
    tr_id = IntField(unique=True)

    meta = {
        'abstract': True,
    }

    def __str__(self):
        val = str(self.tr_id)
        if hasattr(self, 'name'):
            val = '{0}: {1}'.format(val, self.name)
        elif hasattr(self, 'title'):
            val = '{0}: {1}'.format(val, self.title)
        return val

    def save(self, *args, **kwargs):
        # mongoengine doesn't allow "id" field with integer value.
        # It would be possible to declare it as primary_key, but then it's
        # not possible to have ReferenceField while it's not
        # bson.ObjectId()
        tr_id = getattr(self, 'id', None)
        if tr_id:
            setattr(self, 'tr_id', tr_id)
            delattr(self, 'id')
        super(TestRailDocument, self).save(*args, **kwargs)


class Users(TestRailDocument):
    report_fields = [
        'id',
        'email',
        'is_active',
        'name',
    ]


class CaseTypes(TestRailDocument):
    report_fields = [
        'id',
        'is_default',
        'name',
    ]


class Priorities(TestRailDocument):
    report_fields = [
        'id',
        'is_default',
        'name',
        'priority',
        'short_name',
    ]


class Statuses(TestRailDocument):
    report_fields = [
        'id',
        'is_final',
        'is_system',
        'is_untested',
        'label',
        'name',
    ]


class Projects(TestRailDocument):
    report_fields = [
        'id',
        'announcement',
        'completed_on',
        'is_completed',
        'name',
        'show_announcement',
        'suite_mode',
        'url',
    ]

    completed_on = DateTimeField()

    def clean(self):
        if not isinstance(self.completed_on, datetime):
            self.completed_on = timestamp_to_utc(self.completed_on)


class Milestones(TestRailDocument):
    report_fields = [
        'id',
        'completed_on',
        'description',
        'due_on',
        'is_completed',
        'name',
        'project',
        'url',
    ]

    project_id = IntField(required=True, null=True)
    completed_on = DateTimeField()
    due_on = DateTimeField()

    def clean(self):
        if self.completed_on:
            self.completed_on = timestamp_to_utc(self.completed_on)
        if self.due_on:
            self.due_on = timestamp_to_utc(self.due_on)


class Plans(TestRailDocument):
    report_fields = [
        'id',
        'assignedto',
        'blocked_count',
        'completed_on',
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
        'is_completed',
        'milestone',
        'name',
        'passed_count',
        'project',
        'retest_count',
        'untested_count',
        'url',
    ]

    assignedto_id = IntField(null=True)
    created_on = DateTimeField()
    completed_on = DateTimeField()
    created_by = IntField(null=True)
    milestone_id = IntField(null=True)
    project_id = IntField(required=True, null=True)

    def clean(self):
        if self.created_on:
            self.created_on = timestamp_to_utc(self.created_on)
        if self.completed_on:
            self.completed_on = timestamp_to_utc(self.completed_on)


class Configs(TestRailDocument):
    report_fields = [
        'id',
        'configs',
        'name',
        'project',
    ]

    project_id = IntField(required=True, null=True)


class Suites(TestRailDocument):
    report_fields = [
        'id',
        'completed_on',
        'description',
        'is_baseline',
        'is_completed',
        'is_master',
        'name',
        'project',
        'url',
    ]

    project_id = IntField(required=True, null=True)
    completed_on = DateTimeField()

    def clean(self):
        if self.completed_on:
            self.completed_on = timestamp_to_utc(self.completed_on)


class Sections(TestRailDocument):
    report_fields = [
        'id',
        'depth',
        'description',
        'display_order',
        'parent_id',
        'name',
        'suite_id',
        'suite',
    ]

    suite_id = IntField(required=True, null=True)


class Cases(TestRailDocument):
    report_fields = [
        'id',
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

    created_by = IntField(null=True)
    created_on = DateTimeField()
    milestone_id = IntField(null=True)
    priority_id = IntField(null=True)
    section_id = IntField(null=True)
    suite_id = IntField(required=True, null=True)
    type_id = IntField(null=True)
    updated_by = IntField(null=True)
    updated_on = DateTimeField()

    def clean(self):
        if self.created_on:
            self.created_on = timestamp_to_utc(self.created_on)
        if self.updated_on:
            self.updated_on = timestamp_to_utc(self.updated_on)


class Runs(TestRailDocument):
    report_fields = [
        'id',
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

    assignedto_id = IntField(null=True)
    config = StringField(null=True)
    created_by = IntField(null=True)
    created_on = DateTimeField()
    completed_on = DateTimeField()
    milestone_id = IntField(null=True)
    plan_id = IntField(null=True)
    project_id = IntField(required=True, null=True)
    suite_id = IntField(null=True)
    custom_qa_team = StringField(null=True)

    def clean(self):
        if self.created_on:
            self.created_on = timestamp_to_utc(self.created_on)
        if self.completed_on:
            self.completed_on = timestamp_to_utc(self.completed_on)


class Tests(TestRailDocument):
    report_fields = [
        'id',
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

    assignedto_id = IntField(null=True)
    case_id = IntField(null=True)
    milestone_id = IntField(null=True)
    priority_id = IntField(null=True)
    run_id = IntField(required=True, null=True)
    type_id = IntField(null=True)


class Results(TestRailDocument):
    report_fields = [
        'id',
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

    assignedto_id = IntField(null=True)
    created_by = IntField(null=True)
    created_on = DateTimeField()
    test_id = IntField(required=True, null=True)

    def clean(self):
        if self.created_on:
            self.created_on = timestamp_to_utc(self.created_on)


class Syncs(Document):
    started = DateTimeField(required=True)
    finished = DateTimeField()

    def __str__(self):
        return '{0} - {1}'.format(get_dt_iso(self.started),
                                  get_dt_iso(self.finished) or '...')


class Reports(Document):
    created = DateTimeField(default=datetime.now)
    filename = StringField(required=True)
    created_by = ReferenceField(AuthUser)

    def __str__(self):
        return self.filename
