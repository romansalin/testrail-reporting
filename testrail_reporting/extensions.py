from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mongoengine import MongoEngine
from flask.ext.oauthlib.client import OAuth
from flask.ext.restful import Api
from flask.ext.security import Security

toolbar = DebugToolbarExtension()
oauth = OAuth()
cache = Cache()
api = Api()
db = MongoEngine()
security = Security()
