from flask_restful import Resource

from testrail_reporting.extensions import api


class TestRuns(Resource):
    def get(self):
        return {
            'hello': 'world'
        }


api.add_resource(TestRuns, '/reports/run_status')
