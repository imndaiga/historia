from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_script import Command
from . import login_manager
import networkx as nx
import os


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
            if weight in self.directed_types:
                e1_present = GlobalEdge.query.filter_by(
                    ascendant_id=self.id).filter_by(
                    descendant_id=node.id).first()
                e2_present = GlobalEdge.query.filter_by(
                    ascendant_id=node.id).filter_by(
                    descendant_id=self.id).first()
                if not e1_present and not e2_present:
                    e1 = GlobalEdge(
                        ascendant=self, descendant=node, edge_label=weight)
                    e2 = GlobalEdge(ascendant=node, descendant=self,
                                    edge_label=self.directed_types[weight][1])
                    db.session.add_all([e1, e2])
                    db.session.commit()
                    if weight < self.directed_types[weight][1]:
                        result_dict = GlobalGraph().update(
                            edge_dict={self.id: e1, node.id: e2})
                    else:
                        result_dict = GlobalGraph().update(
                            edge_dict={self.id: e1, node.id: e2})
                elif e1_present and not e2_present:
                    e2 = GlobalEdge(ascendant=node, descendant=self,
                                    edge_label=self.directed_types[weight][1])
                    db.session.add(e2)
                    db.session.commit()
                    if weight < self.directed_types[weight][1]:
                        result_dict = GlobalGraph().update(
                            edge_dict={self.id: e2})
                    else:
                        result_dict = GlobalGraph().update(
                            edge_dict={node.id: e2})
                elif not e1_present and e2_present:
                    e1 = GlobalEdge(
                        ascendant=self, descendant=node, edge_label=weight)
                    db.session.add(e1)
                    db.session.commit()
                    if weight < self.directed_types[weight][1]:
                        result_dict = GlobalGraph().update(
                            edge_dict={self.id: e1})
                    else:
                        result_dict = GlobalGraph().update(
                            edge_dict={node.id: e1})
                else:
                    return None
            elif weight in self.undirected_types:
                e1 = GlobalEdge(ascendant=self, descendant=node,
                                edge_label=weight)
                e2 = GlobalEdge(ascendant=node, descendant=self,
                                edge_label=weight)
                db.session.add_all([e1, e2])
                db.session.commit()
                result_dict = GlobalGraph().update(
                    edge_dict={self.id: e1, node.id: e2})
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
            links = {
                1: [n1, n2, 1],
                2: [n1, n3, 3],
                3: [n1, n4, 3],
                4: [n2, n3, 3],
                5: [n2, n4, 3],
                6: [n3, n4, 2]
            }
            db.session.add_all([n1, n2, n3, n4])
            cls.connect_links(links)
        return None

    @classmethod
    def link_new_member(cls, *args, **kwargs):
        if current_app.config['DEBUG'] or current_app.config['TESTING']:
            if kwargs['type'] == 'daughter':
                links = {
                    1: [args[0], args[4], 3],
                    2: [args[1], args[4], 3],
                    3: [args[2], args[4], 2],
                    4: [args[3], args[4], 2]
                }
                db.session.add(args[4])
                cls.connect_links(links)
            elif kwargs['type'] == 'wife':
                link = {
                    1: [args[0], args[1], 1]
                }
                db.session.add(args[1])
                cls.connect_links(link)
            elif kwargs['type'] == 'child':
                links = {
                    1: [args[0], args[2], 3],
                    2: [args[1], args[2], 3]
                }
                db.session.add_all([args[1], args[2]])
                cls.connect_links(links)

    @staticmethod
    def connect_links(links):
        for link in links:
            ret_item = links[link][0].create_edge(
                links[link][1], weight=links[link][2])
        db.session.commit()
        return ret_item

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
