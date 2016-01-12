from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask import Blueprint


api_bp = Blueprint('api', __name__)
# api = Api(api_bp)


# class TestApi(Resource):
#     def get(self, test_id=None):
#         if todo_id is not None:
#             return STORAGE_ENGINE.get_item(USER_ID, todo_id)
#         return STORAGE_ENGINE.get_items(USER_ID)


# api.add_resource(TestApi, '/tests/', '/tests/<string:test_id>')
