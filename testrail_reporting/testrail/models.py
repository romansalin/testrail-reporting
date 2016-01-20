from testrail_reporting.extensions import db


class TestRailBaseDocument(db.DynamicDocument):
    id = db.IntField(primary_key=True)

    meta = {
        'abstract': True,
    }


class Users(TestRailBaseDocument):
    xlsx_fields = [
        'email',
        'is_active',
        'name',
    ]

    email = db.StringField()
    is_active = db.BooleanField()
    name = db.StringField()


class CaseTypes(TestRailBaseDocument):
    xlsx_fields = [
        'is_default',
        'name',
    ]

    is_default = db.BooleanField()
    name = db.StringField()


class Priorities(TestRailBaseDocument):
    xlsx_fields = [
        'is_default',
        'name',
        'priority',
        'short_name',
    ]

    is_default = db.BooleanField()
    name = db.StringField()
    priority = db.IntField()
    short_name = db.StringField()


class Statuses(TestRailBaseDocument):
    xlsx_fields = [
        'is_final',
        'is_system',
        'is_untested',
        'label',
        'name',
    ]

    is_final = db.BooleanField()
    is_system = db.BooleanField()
    is_untested = db.BooleanField()
    label = db.StringField()
    name = db.StringField()


class Projects(TestRailBaseDocument):
    xlsx_fields = [
        'announcement',
        'completed_on',
        'is_completed',
        'name',
        'show_announcement',
        'suite_mode',
        'url',
    ]

    announcement = db.StringField()
    completed_on = db.DateTimeField()
    is_completed = db.BooleanField()
    name = db.StringField()
    show_announcement = db.IntField()
    suite_mode = db.IntField()
    url = db.StringField()


class Milestones(TestRailBaseDocument):
    xlsx_fields = [
        'completed_on',
        'description',
        'due_on',
        'is_completed',
        'name',
        'project_id',
        'url',
    ]

    completed_on = db.DateTimeField()
    description = db.StringField()
    due_on = db.DateTimeField()
    is_completed = db.BooleanField()
    name = db.StringField()
    project_id = db.IntField()
    url = db.StringField()


class Plans(TestRailBaseDocument):
    xlsx_fields = [
        'assignedto_id',
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
        'milestone_id',
        'name',
        'passed_count',
        'project_id',
        'retest_count',
        'untested_count',
        'url',
    ]


class Configs(TestRailBaseDocument):
    xlsx_fields = [
        'configs',
        'name',
        'project_id',
    ]


class Suites(TestRailBaseDocument):
    xlsx_fields = [
        'completed_on',
        'description',
        'is_baseline',
        'is_completed',
        'is_master',
        'name',
        'project_id',
        'url',
    ]


class Sections(TestRailBaseDocument):
    xlsx_fields = [
        'depth',
        'description',
        'display_order',
        'parent_id',
        'name',
        'suite_id',
    ]


class Cases(TestRailBaseDocument):
    xlsx_fields = [
        'created_by',
        'created_on',
        'estimate',
        'estimate_forecast',
        'milestone_id',
        'priority_id',
        'refs',
        'section_id',
        'suite_id',
        'title',
        'type_id',
        'updated_by',
        'updated_on',
    ]


class Runs(TestRailBaseDocument):
    xlsx_fields = [
        'assignedto_id',
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
        'milestone_id',
        'plan_id',
        'name',
        'passed_count',
        'project_id',
        'retest_count',
        'suite_id',
        'untested_count',
        'url',
    ]


class Tests(TestRailBaseDocument):
    xlsx_fields = [
        'assignedto_id',
        'case_id',
        'estimate',
        'estimate_forecast',
        'milestone_id',
        'priority_id',
        'refs',
        'run_id',
        'status_id',
        'title',
        'type_id',
    ]


class Results(TestRailBaseDocument):
    xlsx_fields = [
        'assignedto_id',
        'comment',
        'created_by',
        'created_on',
        'defects',
        'elapsed',
        'status_id',
        'test_id',
        'version',
    ]
