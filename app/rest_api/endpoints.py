from . import api
from flask_restful import Resource
from .decorators import requires_auth
from .. import graph
from ..models import Person
from flask import _app_ctx_stack


class pingAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return 'Here is a ping'

    def put(self):
        return 'Here is a ping'

    def delete(self):
        return 'Here is a ping'

# relation_name:{value:'Father', type:'multiselect-input'},
# birth_date:{value:'2017-02-15', type:'pikaday-input'}


class relationshipsAPI(Resource):
    decorators = [requires_auth]

    def format_response(self, nodes, user_id):
        relations = []
        for node in nodes:
            if node != user_id:
                relation = Person.query.get(node)
                relations.append({
                    'id': {'value': relation.id, 'type': 'hidden-input',
                           'input_name': 'data_id', 'label': 'ID'},
                    'first_name': {'value': relation.baptism_name,
                                   'type': 'alpha-input',
                                   'input_name': 'mod_first-name',
                                   'label': 'First Name'},
                    'ethnic_name': {'value': relation.ethnic_name,
                                    'type': 'alpha-input',
                                    'input_name': 'mod_ethnic-name',
                                    'label': 'Ethnic Name'},
                    'last_name': {'value': relation.surname,
                                  'type': 'alpha-input',
                                  'input_name': 'mod_last-name',
                                  'label': 'Last Name'},
                    'email': {'value': relation.email,
                              'type': 'email-input',
                              'input_name': 'mod_email',
                              'label': 'Email'}
                })
        return relations

    def get(self):
        user_email = _app_ctx_stack.top.current_user['email']
        user = Person.query.filter_by(email=user_email).first()
        node_list = graph.get_subgraph(user).nodes()
        response = self.format_response(node_list, user.id)
        return response

    def put(self):
        return 'Relationship added/updated'

    def delete(self):
        return 'Relationship deleted'


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(pingAPI, '/ping', endpoint='ping')
