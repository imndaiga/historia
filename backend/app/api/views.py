from . import api
from flask_restful import Resource, reqparse
from .decorators import requires_auth
from .. import graph, db
from ..models import Person, Link
from flask import _app_ctx_stack
from sqlalchemy import or_
from networkx import NetworkXError
from networkx.readwrite import json_graph
import random
import math


class pingAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return 'Here is a ping'

    def put(self):
        return 'Here is a ping'

    def delete(self):
        return 'Here is a ping'


class graphAPI(Resource):
    decorators = [requires_auth]

    def getNodeColor(self, node_id):
        current_user_email = _app_ctx_stack.top.current_user['email']
        current_user = Person.query.filter_by(email=current_user_email).first()
        if current_user.id == node_id:
            return '#f96060'
        return '#5c61ad'

    def formatResponse(self, current_user_graph):
        # The NetworkX JSON-transform maps zero-indexed node references in the
        # links list by default. A mapping is necessary to populate json graph
        # with actual node ids for sigmajs to utilise json graph.
        # http://stackoverflow.com/a/38765461
        serialised_graph = json_graph.node_link_data(current_user_graph)
        serialised_graph.pop('graph', None)
        serialised_graph.pop('multigraph', None)
        serialised_graph.pop('directed', None)
        serialised_graph['links'] = [
            {
                'source': serialised_graph['nodes'][link['source']]['id'],
                'target': serialised_graph['nodes'][link['target']]['id'],
                'weight': link['weight']
            }
            for link in serialised_graph['links']
        ]
        serialised_graph['nodes'] = [
            {
                'id': node['id'],
                'label': Person.query.filter_by(
                    id=node['id']).first().baptism_name,
                'x': random.randrange(1, 10),
                'y': random.randrange(1, 10),
                'color': self.getNodeColor(node['id']),
                'size': 2
            }
            for node in serialised_graph['nodes']
        ]
        serialised_graph['edges'] = serialised_graph.pop('links', None)
        for count, edge in enumerate(serialised_graph['edges']):
            edge['id'] = count
        return serialised_graph

    def get(self):
        current_user_email = _app_ctx_stack.top.current_user['email']
        current_user = Person.query.filter_by(
            email=current_user_email).first()
        print('Returning graph for node {}'.format(current_user.id))
        current_user_graph = graph.get_subgraph(current_user)
        json_graph = self.formatResponse(current_user_graph)
        return {'graph': json_graph}


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

# relation_name:{value:'Father', type:'multiselect-input'},
# birth_date:{value:'2017-02-15', type:'pikaday-input'}


class relationshipsAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data', type=dict, location='json')
        self.reqparse.add_argument('user_id', type=int, location='json')
        self.reqparse.add_argument('page', type=str, location='args')
        self.relationships_per_page = 10
        super(relationshipsAPI, self).__init__()

    def formatResponse(self, page, nodes):
        relatives = []
        for node in nodes:
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
                    'type': 'alpha-input', 'value':
                        relation.surname or '',
                    'label': 'Last Name',
                    'validators': ['required', 'alpha'],
                    'field_name': 'last_name'
                },
                {
                    'type': 'email-input', 'value':
                        relation.email or '',
                    'label': 'Email', 'validators':
                        ['required', 'email'],
                    'field_name': 'email'
                }
            ])
        return relatives

    def get(self):
        user_email = _app_ctx_stack.top.current_user['email']
        args = self.reqparse.parse_args()
        page = 1 if not args['page'] else int(args['page'])
        user = Person.query.filter_by(email=user_email).first()
        node_list = graph.get_subgraph(user).nodes()
        for node in node_list:
            if node == user.id:
                del node_list[node]
        max_page = math.ceil(len(node_list) / self.relationships_per_page)
        max_rows = page * self.relationships_per_page
        max_index = max_rows \
            if page < max_page else None
        min_index = max_rows - self.relationships_per_page \
            if page < max_page or max_rows == len(node_list) \
            else len(node_list) - self.relationships_per_page
        node_list = node_list[min_index: max_index]
        response = {
            'current_page': page,
            'last_page': max_page,
            'prev_page_url': 'null' if not page
                             else 'api/relationships?page=' +
                                  str(int(page) - 1),
            'next_page_url': 'null' if page == max_page
                             else 'api/relationships?page=' +
                                  str(int(page) + 1),
            'data': []
        }
        response['data'] = self.formatResponse(page, node_list)
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
                response = self.formatResponse(node_list)
                print('{} deleted from graph'.format(delete_person_id))
                return response
            except NetworkXError:
                print('{} does not exist in graph'.format(delete_person_id))
                return {}
        print('{} does not exist in database'.format(delete_person_id))
        return {}


class personAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, location='json')
        super(personAPI, self).__init__()

    def get(self):
        pass

    def put(self):
        pass


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(searchAPI, '/search', endpoint='search')
api.add_resource(graphAPI, '/graph', endpoint='graph')
api.add_resource(personAPI, '/person', endpoint='person')
api.add_resource(pingAPI, '/ping', endpoint='ping')
