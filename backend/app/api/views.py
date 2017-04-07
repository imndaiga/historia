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

    def __init__(self):
        self.user_id = _app_ctx_stack.top.current_user['id']
        self.current_user = Person.query.filter_by(id=self.user_id).first()
        super(graphAPI, self).__init__()

    def getNodeColor(self, node_id):
        if self.current_user.id == node_id:
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
        print('Returning graph for node {}'.format(self.current_user.id))
        current_user_graph = graph.get_subgraph(self.current_user)
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


class relationshipsAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.user_id = _app_ctx_stack.top.current_user['id']
        self.current_user = Person.query.filter_by(id=self.user_id).first()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data', type=dict, location='json')
        self.reqparse.add_argument('id', type=int, location='json')
        self.reqparse.add_argument('page', type=str, location='args')
        self.reqparse.add_argument('type', type=str, location='args')
        self.relationships_per_page = 10
        super(relationshipsAPI, self).__init__()

    def formatResponse(self, nodes):
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
        args = self.reqparse.parse_args()
        page = 1 if not args['page'] else int(args['page'])
        node_list = graph.get_subgraph(self.current_user).nodes()
        for index, node in enumerate(node_list):
            if node == self.current_user.id:
                del node_list[index]
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
        response['data'] = self.formatResponse(node_list)
        return response

    def put(self):
        args = self.reqparse.parse_args()
        print(args.data['form'])
        return {'message': 'Relationship added/updated'}

    def delete(self):
        args = self.reqparse.parse_args()
        delete_person_id = args['id']
        deleted_uid = Person.query.filter_by(id=delete_person_id).delete()
        if deleted_uid == 1:
            print('{} deleted from database'.format(delete_person_id))
            try:
                Link.query.filter(
                    or_(Link.ascendant_id == delete_person_id,
                        Link.descendant_id == delete_person_id)).delete()
                db.session.commit()
                graph.delete_node(delete_person_id)
                print('{} deleted from graph'.format(delete_person_id))
                return {'message': 'Relationship deleted'}
            except NetworkXError:
                print('{} does not exist in graph'.format(delete_person_id))
                return {'message': 'Graph error'}
        else:
            print('{} does not exist in database'.format(delete_person_id))
            return {'message': 'Database error'}


class personAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        super(personAPI, self).__init__()

    def formatResponse(self, person):
        relative = [
            {
                'type': 'hidden-input', 'value': person.id or '',
                'label': 'ID', 'field_name': 'id'
            },
            {
                'type': 'alpha-input',
                'value': person.baptism_name or '',
                'label': 'First Name',
                'validators': ['required', 'alpha'],
                'field_name': 'first_name'
            },
            {
                'type': 'alpha-input',
                'value': person.ethnic_name or '',
                'label': 'Ethnic Name',
                'validators': ['required', 'alpha'],
                'field_name': 'ethnic_name'},
            {
                'type': 'alpha-input', 'value':
                    person.surname or '',
                'label': 'Last Name',
                'validators': ['required', 'alpha'],
                'field_name': 'last_name'
            },
            {
                'type': 'email-input', 'value':
                    person.email or '',
                'label': 'Email', 'validators':
                    ['required', 'email'],
                'field_name': 'email'
            },
            {
                'type': 'pikaday-input', 'value':
                    str(person.dob) or '',
                'label': 'Date of Birth', 'validators':
                    [],
                'field_name': 'birth_date'
            }
        ]
        return {'form': relative, 'inline': False}

    def get(self):
        args = self.reqparse.parse_args()
        person_id = args['id']
        person = Person.query.filter_by(id=person_id).one()
        return self.formatResponse(person)


class familyAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        super(familyAPI, self).__init__()

    def formatResponse(self, relations_list):
        family_array = []
        for relation_tree in relations_list:
            for relation_degree in relation_tree:
                target_id = relation_degree[0]
                relation = relation_degree[1]
                target = Person.query.get(target_id)
                listed_names = [
                    target.baptism_name or '',
                    target.ethnic_name or '',
                    target.surname or ''
                ]
                target_fullname = ' '.join(filter(None, listed_names))
                family_array.append(
                    {
                        'type': 'multiselect-input',
                        'placeholder': relation,
                        'value': relation,
                        'label': 'Relation',
                        'validators': ['required'],
                        'field_name': 'to_relation_' + str(target_id),
                        'multiselect_options': [
                            'Parent', 'Sibling', 'Step-Parent',
                            'Step-Sibling', 'Child'
                        ],
                        'classes': 'col-lg-6 col-md-6 col-sm-6 col-xs-12' +
                                   ' inline-split',
                        'SelectLabel': '',
                        'DeselectLabel': ''
                    }
                )
                family_array.append(
                    {
                        'type': 'search-input',
                        'placeholder': 'Search for Relative',
                        'value': target_fullname,
                        'label': 'To',
                        'validators': ['required'],
                        'field_name': 'to_fullname_' + str(target_id),
                        'classes': 'col-lg-6 col-md-6 col-sm-6 col-xs-12',
                        'SelectLabel': '',
                        'DeselectLabel': ''
                    }
                )
        return {'form': family_array, 'inline': True}

    def get(self):
        args = self.reqparse.parse_args()
        person_id = args['id']
        relations_list = []
        if person_id is not None:
            source = Person.query.get(person_id)
            neighbor_list = graph.current.neighbors(person_id)
            for node in neighbor_list:
                target = Person.query.get(node)
                relationship = graph.get_relation_tree(source, target)
                relations_list.append(relationship)
            return self.formatResponse(relations_list)
        return {'message': 'missing person_id'}


class userAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        super(userAPI, self).__init__()

    def get(self):
        pass


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(searchAPI, '/search', endpoint='search')
api.add_resource(graphAPI, '/graph', endpoint='graph')
api.add_resource(personAPI, '/person', endpoint='person')
api.add_resource(familyAPI, '/person/family', endpoint='family')
api.add_resource(userAPI, '/user', endpoint='user')
api.add_resource(pingAPI, '/ping', endpoint='ping')
