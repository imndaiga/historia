from . import api
from flask_restful import Resource, reqparse
from .decorators import requires_auth
from .. import graph, db
from ..models import Person, get_one_or_create
from flask import _app_ctx_stack
from networkx import NetworkXError
from networkx.readwrite import json_graph
from datetime import datetime
import random
import math


def getUser():
    return Person.query.filter_by(
        email=_app_ctx_stack.top.current_user['email']).first()


class graphAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.current_user = getUser()
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
                    id=node['id']).first().first_name,
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
        json_graph = self.formatResponse(self.current_user.get_graph())
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
            first_name=args['value']).first()
        if (found_person is not None):
            print('Person found: {}'.format(found_person))
            listed_names = [
                found_person.first_name or '',
                found_person.ethnic_name or '',
                found_person.last_name or ''
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
        self.current_user = getUser()
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
                    'value': relation.first_name or '',
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
                        relation.last_name or '',
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
        node_list = self.current_user.get_graph().nodes()
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
                db.session.commit()
                graph.GlobalGraph.remove_node(delete_person_id)
                print('{} deleted from graph'.format(delete_person_id))
                return {'person': delete_person_id}
            except NetworkXError:
                print('{} does not exist in graph'.format(delete_person_id))
                return {'person': -1}
        else:
            print('{} does not exist in database'.format(delete_person_id))
            return {'person': -1}


class personAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        self.reqparse.add_argument('data', type=dict, location='json')
        super(personAPI, self).__init__()

    def formatResponse(self, person):
        relative = [
            {
                'type': 'hidden-input', 'value': person.id or '',
                'label': 'ID', 'field_name': 'id'
            },
            {
                'type': 'alpha-input',
                'value': person.first_name or '',
                'label': 'First Name',
                'validators': ['required', 'alpha'],
                'field_name': 'first_name',
                'classes': ''
            },
            {
                'type': 'alpha-input',
                'value': person.ethnic_name or '',
                'label': 'Ethnic Name',
                'validators': ['required', 'alpha'],
                'field_name': 'ethnic_name',
                'classes': ''
            },
            {
                'type': 'alpha-input', 'value':
                    person.last_name or '',
                'label': 'Last Name',
                'validators': ['required', 'alpha'],
                'field_name': 'last_name',
                'classes': ''
            },
            {
                'type': 'email-input', 'value':
                    person.email or '',
                'label': 'Email', 'validators':
                    ['required', 'email'],
                'field_name': 'email',
                'classes': ''
            },
            {
                'type': 'multiselect-input', 'value':
                    str(person.sex) or '',
                'label': 'Sex', 'validators':
                    ['required'],
                'field_name': 'sex',
                'multiselect_options': ['Male', 'Female', 'Other'],
                'SelectLabel': '',
                'DeselectLabel': '',
                'classes': ''
            },
            {
                'type': 'pikaday-input', 'value':
                    str(person.birth_date) or '',
                'label': 'Date of Birth', 'validators':
                    [],
                'field_name': 'birth_date',
                'classes': ''
            }
        ]
        return relative

    def get(self):
        args = self.reqparse.parse_args()
        person_id = args['id']
        person = Person.query.filter_by(id=person_id).one()
        return self.formatResponse(person)

    def put(self):
        args = self.reqparse.parse_args()
        form = args.data['form']
        birth_date = datetime.strptime(
            form['birth_date'], '%b %d %Y')
        created_person, exists = get_one_or_create(
            session=db.session,
            model=Person,
            create_method='create_from_email',
            create_method_kwargs={
                'first_name': form['first_name'],
                'ethnic_name': form['ethnic_name'],
                'last_name': form['last_name'],
                'sex': form['sex'],
                'birth_date': birth_date
            },
            email=form['email']
        )
        if not exists:
            db.session.commit()
            return {'person': created_person.id}
        else:
            return {'person': -1}


class familyAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        super(familyAPI, self).__init__()

    def formatResponse(self, relations_list):
        family_array = []
        for relationship in relations_list:
            target_id = relationship[0]
            relation = relationship[1]
            target = Person.query.get(target_id)
            listed_names = [
                target.first_name or '',
                target.ethnic_name or '',
                target.last_name or ''
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
                    'classes': 'col-lg-6 col-md-6 col-sm-6 col-xs-12',
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
        return family_array

    def get(self):
        args = self.reqparse.parse_args()
        source_id = args['id']
        relations_list = []

        if source_id:
            neighbour_list = graph.GlobalGraph.neighbors(source_id)
            for target_id in neighbour_list:
                relations_list.append([
                    target_id, graph.get_relationship(source_id, target_id)
                ])
            return self.formatResponse(relations_list)
        return {'message': 'missing person_id'}


class statisticsAPI(Resource):
    decorators = [requires_auth]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='args')
        super(statisticsAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        person_id = args['id']
        if person_id is not None:
            user = Person.query.get(person_id)
        else:
            user = getUser()
        nodeSize = user.get_graph().number_of_nodes()
        return {'nodeSize': nodeSize}


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(searchAPI, '/search', endpoint='search')
api.add_resource(graphAPI, '/graph', endpoint='graph')
api.add_resource(personAPI, '/person', endpoint='person')
api.add_resource(familyAPI, '/person/family', endpoint='family')
api.add_resource(statisticsAPI, '/user/statistics', endpoint='statistics')
