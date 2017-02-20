from . import api
from flask_restful import Resource
from .decorators import requires_auth


class UserAPI(Resource):

    def get(self, id):
        return "Hello, World!"

    def put(self, id):
        pass

    def delete(self, id):
        pass


class pingAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return 'Here is a ping'

    def put(self):
        return 'Ping updated'

    def delete(self):
        return 'Ping deleted'


api.add_resource(pingAPI, '/ping', endpoint='ping')
api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
