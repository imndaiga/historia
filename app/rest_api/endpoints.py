from . import api
from flask_restful import Resource
from .decorators import requires_auth
from .. import graph, db
from ..models import Person, Link
from flask import _app_ctx_stack, request
from sqlalchemy import or_


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
        relatives = []
        for node in nodes:
            if node != user_id:
                relation = Person.query.get(node)
                relatives.append([
                    {
                        'type': 'hidden-input', 'value': relation.id or '',
                        'label': 'ID', 'field_name': 'id'
                    },
                    {
                        'type': 'alpha-input',
                        'value': relation.baptism_name or '',
                        'label': 'First Name',
                        'validators': ['required', 'alpha'],
                        'field_name': 'first_name'
                    },
                    {
                        'type': 'alpha-input',
                        'value': relation.ethnic_name or '',
                        'label': 'Ethnic Name',
                        'validators': ['required', 'alpha'],
                        'field_name': 'ethnic_name'},
                    {
                        'type': 'alpha-input', 'value': relation.surname or '',
                        'label': 'Last Name',
                        'validators': ['required', 'alpha'],
                        'field_name': 'last_name'
                    },
                    {
                        'type': 'email-input', 'value': relation.email or '',
                        'label': 'Email', 'validators': ['required', 'email'],
                        'field_name': 'email'
                    }
                ])
        return relatives

    def get(self):
        user_email = _app_ctx_stack.top.current_user['email']
        user = Person.query.filter_by(email=user_email).first()
        node_list = graph.get_subgraph(user).nodes()
        response = self.format_response(node_list, user.id)
        return response

    def put(self):
        print(request.get_json('data'))
        return {'message': 'Relationship added/updated'}

    def delete(self):
        user_email = _app_ctx_stack.top.current_user['email']
        delete_person_id = int(request.data)
        user = Person.query.filter_by(email=user_email).first()
        Person.query.filter_by(id=delete_person_id).delete()
        Link.query.filter(
            or_(Link.ascendant_id == delete_person_id,
                Link.descendant_id == delete_person_id)).delete()
        db.session.commit()
        graph.delete_node(delete_person_id)
        node_list = graph.get_subgraph(user).nodes()
        response = self.format_response(node_list, user.id)
        return response


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(pingAPI, '/ping', endpoint='ping')
