from testrail_reporting.extensions import db


class Projects(db.Document):
    id = db.IntField(primary_key=True)
    announcement = db.StringField()
    is_completed = db.BooleanField()
    completed_on = db.StringField(),
    name = db.StringField()
    show_announcement = db.IntField()
    suite_mode = db.IntField()
    url = db.StringField()


class Users(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class CaseTypes(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Priorities(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Statuses(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Milestones(db.Document):
    id = db.IntField(primary_key=True)
    description = db.StringField()
    is_completed = db.BooleanField()
    completed_on = db.StringField()
    name = db.StringField()
    project_id = db.IntField()
    url = db.StringField()
    due_on = db.IntField()


class Plans(db.Document):
    # entries?
    id = db.IntField(primary_key=True)
    assignedto_id = db.IntField()
    blocked_count = db.IntField()
    completed_on = db.IntField()
    created_by = db.IntField()
    created_on = db.IntField()
    custom_status1_count = db.IntField()
    custom_status2_count = db.IntField()
    custom_status3_count = db.IntField()
    custom_status4_count = db.IntField()
    custom_status5_count = db.IntField()
    custom_status6_count = db.IntField()
    custom_status7_count = db.IntField()
    description = db.StringField()
    failed_count = db.IntField()
    is_completed = db.BooleanField()
    milestone_id = db.IntField()
    name = db.StringField()
    passed_count = db.IntField()
    project_id = db.IntField()
    retest_count = db.IntField()
    untested_count = db.IntField()
    url = db.StringField()


class Configs(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Suites(db.Document):
    id = db.IntField(primary_key=True)
    is_baseline = db.BooleanField()
    is_completed = db.BooleanField()
    is_master = db.BooleanField()
    name = db.StringField()
    project_id = db.IntField()
    url = db.StringField()


class Sections(db.Document):
    id = db.IntField(primary_key=True)
    depth
    display_order
    name
    suite_id


class Cases(db.Document):
    id = db.IntField(primary_key=True)
    created_by = db.IntField()
    created_on = db.IntField()
    custom_test_case_description = db.StringField()
    custom_test_case_steps = db.StringField()
    custom_test_group = db.StringField()
    estimate = db.StringField()
    estimate_forecast = db.StringField()
    milestone_id = db.IntField()
    priority_id = db.IntField()
    section_id = db.IntField()
    suite_id = db.IntField()
    title = db.StringField()
    type_id = db.IntField()
    updated_by = db.IntField()
    updated_on = db.IntField()


class Runs(db.Document):
    id = db.IntField(primary_key=True)
    blocked_count
    config_ids
    created_by
    created_on
    custom_status1_count
    custom_status2_count
    custom_status3_count
    custom_status4_count
    custom_status5_count
    custom_status6_count
    custom_status7_count
    failed_count
    include_all
    is_completed
    name
    passed_count
    project_id
    retest_count
    suite_id
    untested_count
    url


class Tests(db.Document):
    id = db.IntField(primary_key=True)
    case_id
    custom_case_complexity
    custom_qa_team
    custom_test_case_description
    custom_test_case_steps
    milestone_id
    priority_id
    run_id
    status_id
    title
    type_id


class Results(db.Document):
    id = db.IntField(primary_key=True)
    created_by
    created_on
    custom_stdev
    custom_test_case_steps_results
    custom_throughput
    status_id
    test_id
