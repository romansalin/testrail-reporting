from testrail_reporting.extensions import db


class Projects(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Users(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class CaseTypes(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Priorities(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Statuses(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Milestones(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Plans(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Configurations(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Suites(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Sections(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Cases(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Runs(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Tests(db.DynamicDocument):
    id = db.IntField(primary_key=True)


class Results(db.DynamicDocument):
    id = db.IntField(primary_key=True)
