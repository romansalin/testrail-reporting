from testrail_reporting.extensions import db


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


class Configs(TestRailBaseDocument):
    report_fields = [
        '_id',
        'configs',
        'name',
        'project',
    ]


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
    ]


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
