from . import api
from flask_restful import Resource, reqparse
from .decorators import requires_auth
from .. import graph, db
from ..models import Person, Link
from flask import _app_ctx_stack
from sqlalchemy import or_
from networkx import NetworkXError


class pingAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return 'Here is a ping'

    def put(self):
        return 'Here is a ping'

    def delete(self):
        return 'Here is a ping'


class searchAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('field', type=str,
                                   location='args', required=True)
        self.reqparse.add_argument('value', type=str,
                                   location='args', required=True)
        super(searchAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        found_person = db.session.query(Person).filter_by(
            baptism_name=args['value']).first()
        if (found_person is not None):
            print('Person found: {}'.format(found_person))
            listed_names = [
                found_person.baptism_name or '',
                found_person.ethnic_name or '',
                found_person.surname or ''
            ]
            person_fullname = ' '.join(filter(None, listed_names))
            print({'fullname': person_fullname,
                   'id': found_person.id})

            return {'fullname': person_fullname,
                    'id': found_person.id}
        return {}

    def put(self):
        pass

    def delete(self):
        pass

# relation_name:{value:'Father', type:'multiselect-input'},
# birth_date:{value:'2017-02-15', type:'pikaday-input'}


class relationshipsAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data', type=dict, location='json')
        self.reqparse.add_argument('user_id', type=int, location='json')
        super(relationshipsAPI, self).__init__()

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
        args = self.reqparse.parse_args()
        print(args.data['form'])
        return {'message': 'Relationship added/updated'}

    def delete(self):
        args = self.reqparse.parse_args()
        print(args)
        user_email = _app_ctx_stack.top.current_user['email']
        delete_person_id = args['user_id']
        user = Person.query.filter_by(email=user_email).first()
        deleted_uid = Person.query.filter_by(id=delete_person_id).delete()
        if deleted_uid == 1:
            print('{} deleted from database'.format(delete_person_id))
            try:
                Link.query.filter(
                    or_(Link.ascendant_id == delete_person_id,
                        Link.descendant_id == delete_person_id)).delete()
                db.session.commit()
                graph.delete_node(delete_person_id)
                node_list = graph.get_subgraph(user).nodes()
                response = self.format_response(node_list, user.id)
                print('{} deleted from graph'.format(delete_person_id))
                return response
            except NetworkXError:
                print('{} does not exist in graph'.format(delete_person_id))
                return {}
        print('{} does not exist in database'.format(delete_person_id))
        return {}


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(searchAPI, '/search', endpoint='search')
api.add_resource(pingAPI, '/ping', endpoint='ping')
