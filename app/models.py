from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_script import Command
from . import login_manager
import networkx as nx
import os
from sqlalchemy import or_, and_


class GlobalEdge(db.Model):
    """self-referential association table that connects Nodes"""
    __tablename__ = 'edges'

    def __init__(self, edge_label, **kwargs):
        super(GlobalEdge, self).__init__(**kwargs)
        self.edge_label = edge_label

    ascendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
                             primary_key=True)
    descendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
                              primary_key=True)
    edge_label = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<GlobalEdge %s-%s:%s>' % (self.ascendant_id,
                                          self.descendant_id, self.edge_label)


class Node(db.Model, UserMixin):
    """all miminani subscribed Nodes"""
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    baptism_name = db.Column(db.String(64))
    ethnic_name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(64))
    dob = db.Column(db.DateTime, default=date(9999, 1, 1))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    descended_by = db.relationship('GlobalEdge',
                                   foreign_keys=[GlobalEdge.ascendant_id],
                                   backref=db.backref(
                                       'ascendant', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    ascended_by = db.relationship('GlobalEdge',
                                  foreign_keys=[GlobalEdge.descendant_id],
                                  backref=db.backref(
                                      'descendant', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')

    directed_types = {3: ['parent', 4], 4: ['child', 3]}
    undirected_types = {1: ['partner'], 2: ['sibling', 3]}
    relation_dict = {
        1: 'partner',
        2: 'sibling',
        3: 'parent',
        4: 'child',
        5: 'nibling',
        6: 'uncle-aunt'
    }

    @property
    def subgraph(self):
        return self._create_subgraph()[1]

    def generate_login_token(self, email, remember_me=False,
                             next_url=None, expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'login': self.id, 'remember_me': remember_me,
                        'next_url': next_url, 'email': email})

    def confirm_login(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('login') != self.id:
            return False
        return {'remember_me': data.get('remember_me'),
                'next_url': data.get('next_url')}

    def edge_ascends(self, node):
        return self.descended_by.filter_by(
            descendant_id=node.id).first() is not None

    def edge_descends(self, node):
        return self.ascended_by.filter_by(
            ascendant_id=node.id).first() is not None

    def create_edge(self, node, weight):
        result_dict = {}

        if self.baptism_name != node.baptism_name:
            if weight in self.undirected_types or \
               weight in self.directed_types:
                edge_in_db = GlobalEdge.query.filter(
                    and_(GlobalEdge.ascendant == self,
                         GlobalEdge.descendant == node,
                         GlobalEdge.edge_label == weight)).first()
                if edge_in_db is None:
                    e1 = GlobalEdge(ascendant=self, descendant=node,
                                    edge_label=weight)
                    db.session.add(e1)
                    db.session.commit()
                    result_dict = GlobalGraph().update(
                        edge_dict={self.id: e1})
            else:
                return None
            return result_dict
        else:
            return None

    def _create_subgraph(self, gtype=nx.Graph):
        subgraph = gtype()
        weighted_edge_list = self._resolve_edge_list_from_mdg(
            GlobalGraph().current)
        subgraph.add_weighted_edges_from(weighted_edge_list)
        return (self, subgraph)

    # This function should be protected
    def _change_edge_label(self, node, edge_label):
        if self.baptism_name != node.baptism_name:
            if self.edge_ascends(node):
                n = GlobalEdge.query.filter_by(descendant_id=node.id).first()
            elif self.edge_descends(node):
                n = GlobalEdge.query.filter_by(ascendant_id=node.id).first()
            else:
                # Self and Node are not related, no edge_label change can be
                # made
                return None
            n.edge_label = edge_label
            db.session.add(n)
            return n
        return None

    def _resolve_relation(self, target):
        relation_list = []
        weighted_edge_list = self._span_mdg(
            GlobalGraph().current, mutate=True).get(target.id)
        if weighted_edge_list:
            for edge_tuple in weighted_edge_list:
                (node_id, weight) = edge_tuple
                for relation in self.relation_dict:
                    if weight == relation:
                        relation_list.append(self.relation_dict[relation])
            return relation_list
        else:
            return None

    def _resolve_edge_list_from_mdg(self, input_MDG):
        edges = []
        path_inputs = self._span_mdg(input_MDG)
        for node_id in path_inputs:
            set_node_id = None
            if len(path_inputs[node_id]) == 1:
                (_, weight_to_selfid) = path_inputs[node_id][0]
                edges.append((self.id, node_id, weight_to_selfid))
            elif len(path_inputs[node_id]) > 1:
                for path_tuples in path_inputs[node_id]:
                    if set_node_id is None:
                        (set_node_id, weight_to_selfid) = path_tuples
                    else:
                        (new_node_id, sum_weight) = path_tuples
                        new_weight = sum_weight - weight_to_selfid
                        edges.append((set_node_id, new_node_id, new_weight))
                        (set_node_id, weight_to_selfid) = path_tuples
        return edges

    def _span_mdg(self, input_MDG, mutate=False):
        ret_dict = {}
        for u_id, nbrs in input_MDG.adjacency_iter():
            for v_id, keydict in nbrs.items():
                if u_id == self.id:
                    ret_dict[v_id] = list(
                        [(u_id, input_MDG[u_id][v_id][u_id]['weight'])])
                elif u_id != self.id and v_id != self.id:
                    if u_id not in ret_dict:
                        _selfid_to_uid_path = self._evaluate_path_in_mdg(
                            input_MDG, u_id)
                        if _selfid_to_uid_path is not None:
                            if mutate:
                                mut_paths = self._mutate_to_sequential_paths(
                                    _selfid_to_uid_path)
                                ret_dict[u_id] = mut_paths
                            else:
                                ret_dict[u_id] = _selfid_to_uid_path
        return ret_dict

    def _mutate_to_sequential_paths(self, list_of_edge_tuples):
        ret_list = []
        prev_node_id = -99
        for half_edge in list_of_edge_tuples:
            if prev_node_id == -99:
                (prev_node_id, _) = half_edge
                ret_list.append(half_edge)
            else:
                (new_node_id, _) = half_edge
                (weights, _) = nx.single_source_dijkstra(
                    GlobalGraph().current,
                    new_node_id, prev_node_id, weight='weight')
                target_weight = weights.get(prev_node_id)
                mut_half_edge = (new_node_id, target_weight)
                ret_list.append(mut_half_edge)
                (prev_node_id, _) = half_edge
        return ret_list

    def _evaluate_path_in_mdg(self, input_MDG, target_id):
        ret_list = []
        (weights, paths) = nx.single_source_dijkstra(
            input_MDG, self.id, target_id, weight='weight')
        target_path = paths.get(target_id)
        if target_path is not None:
            for node_id in target_path:
                if node_id != self.id:
                    ret_list.append((node_id, weights.get(node_id)))
            return ret_list
        else:
            return None

    @staticmethod
    def node_from_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return {'sig': False, 'node': None}
        if data.get('email'):
            return {'sig': True, 'node': Node.query.filter_by(
                email=data.get('email')).first()}
        else:
            return {'sig': False, 'node': None}

    @login_manager.user_loader
    def load_user(user_id):
        return Node.query.get(int(user_id))

    def __repr__(self):
        return 'Node: <%s>' % self.baptism_name


class GlobalGraph:

    def update(self, edge_dict):
        G = self._load()
        for key in edge_dict:
            source = edge_dict[key].ascendant.id
            target = edge_dict[key].descendant.id
            length = edge_dict[key].edge_label
            G.add_edge(source, target, key=key, weight=length)
        self._save(G)
        return {'input': edge_dict, 'output': G}

    @property
    def current(self):
        return self._load()

    def _save(self, G):
        nx.write_gpickle(G, current_app.config['GRAPH_PATH'])

    def _load(self):
        if os.path.exists(current_app.config['GRAPH_PATH']):
            G = nx.read_gpickle(current_app.config['GRAPH_PATH'])
        else:
            G = nx.MultiDiGraph()
        return G


class Seed(Command):
    """Create fake seed data and store in database"""
    # This function should be protected

    @classmethod
    def run(cls):
        if current_app.config['DEBUG'] or current_app.config['TESTING']:
            n1 = Node(baptism_name='Chris', email='chris@family.com',
                      dob=date(1900, 11, 1))
            n2 = Node(baptism_name='Christine',
                      email='christine@family.com', dob=date(1910, 12, 2))
            n3 = Node(baptism_name='Charlie',
                      email='charlie@family.com', dob=date(1925, 10, 3))
            n4 = Node(baptism_name='Carol',
                      email='carol@family.com', dob=date(1930, 8, 4))
            result = cls.relate(parents=[n1, n2], children=[n3, n4])
        return result

    @classmethod
    def relate(cls, partners=None, parents=None, children=None):
        if current_app.config['DEBUG'] or current_app.config['TESTING']:
            if partners and not parents and not children:
                cls._commit_nodes_to_db(partners=partners)
                links = cls._links_constructor(partners=partners)
            elif parents and children and not partners:
                cls._commit_nodes_to_db(parents=parents, children=children)
                links = cls._links_constructor(parents=parents,
                                               children=children)
            else:
                raise Exception('Expects: (**partners)/(**parents,**children)')
        result = cls.connect_links(links)
        return result

    @staticmethod
    def connect_links(links):
        ret_list = []
        for link in links:
            asc = links[link][0]
            descedants = links[link][1:-1]
            weight = links[link][-1]
            for des in descedants:
                created_item = asc.create_edge(des, weight=weight)
                ret_list.append(created_item)
        return ret_list

    @staticmethod
    def _commit_nodes_to_db(**kwargs):
        for node_type in kwargs:
            for node in kwargs[node_type]:
                node_in_db = Node.query.filter_by(id=node.id).first()
                if node_in_db is None:
                    db.session.add(node)
        db.session.commit()

    @staticmethod
    def _post_process_links(preprocessed):
        ret_dict = {}
        _inverse = {}

        if 2 in preprocessed and \
           1 in preprocessed and \
           0 not in preprocessed:

            for i, parent_node in enumerate(preprocessed[1]):
                index = i + 1
                ret_dict[index] = [[parent_node], preprocessed[2], [3]]
                next_index = index + 1
            index = next_index
            for child_node in preprocessed[2]:
                ret_dict[index] = [[child_node], preprocessed[1], [4]]
                index += 1
                next_index = index
            index = next_index

            if len(preprocessed[1]) > 1:
                # ensure self-loop links are not constructed
                for current_index, partner_node in enumerate(preprocessed[1]):
                    _inverse['self'] = preprocessed[1].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[partner_node], _inverse['self'], [1]]
                    _inverse.clear()
                    index += 1
                    next_index = index
                index = next_index
            if len(preprocessed[2]) > 1:
                # ensure self-loop links are not constructed
                for current_index, sibling_node in enumerate(preprocessed[2]):
                    _inverse['self'] = preprocessed[2].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[sibling_node], _inverse['self'], [2]]
                    _inverse.clear()
                    index += 1
        elif 0 in preprocessed and \
                2 not in preprocessed and \
                1 not in preprocessed:

            if len(preprocessed[0]) > 1:
                # ensure self-loop links are not constructed
                index = 1
                for current_index, partner_node in enumerate(preprocessed[0]):
                    _inverse['self'] = preprocessed[0].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[partner_node], _inverse['self'], [1]]
                    _inverse.clear()
                    index += 1

        for nested_list in ret_dict:
            flattened_list = [val
                              for sublist in ret_dict[nested_list]
                              for val in sublist]
            ret_dict[nested_list] = flattened_list
            flattened_list = []

        return ret_dict

    @classmethod
    def _links_constructor(cls, **kwargs):
        _process_dict = {}
        for node_type in kwargs:
            if node_type == 'parents':
                _process_dict[1] = kwargs[node_type]
            elif node_type == 'partners':
                _process_dict[0] = kwargs[node_type]
            elif node_type == 'children':
                _process_dict[2] = kwargs[node_type]

        constructed_link_dict = cls._post_process_links(_process_dict)
        return constructed_link_dict

    @staticmethod
    def count_edge_labels(**kwargs):
        data = kwargs['data']
        counts = {}
        for edge in data:
            if counts.get(edge[2]['weight']):
                counts[edge[2]['weight']] = counts[edge[2]['weight']] + 1
            else:
                counts[edge[2]['weight']] = 1
        return counts
