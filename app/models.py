from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_script import Command
from . import login_manager
import networkx as nx
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


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

    @classmethod
    def safe(cls, ascendant, descendant, edge_label):
        if ascendant != descendant:
            if edge_label in Relations['directed_types'] or \
               edge_label in Relations['undirected_types']:
                return cls(ascendant=ascendant,
                           descendant=descendant,
                           edge_label=edge_label)
        return None

    def __repr__(self):
        return '<GlobalEdge %s-%s:%s>' % (self.ascendant_id,
                                          self.descendant_id,
                                          self.edge_label)


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

    def _create_subgraph(self, gtype=nx.Graph):
        subgraph = gtype()
        weighted_edge_list = self._resolve_edge_list_from_mdg(
            GlobalGraph(current_app).current)
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
            GlobalGraph(current_app).current, mutate=True).get(target.id)
        if weighted_edge_list:
            for edge_tuple in weighted_edge_list:
                (node_id, weight) = edge_tuple
                for relation in Relations['all_types']:
                    if weight == relation:
                        relation_list.append(Relations['all_types'][relation])
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
                    GlobalGraph(current_app).current,
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

    def auto(node, baptism_name):
        return node

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

    def __repr__(self):
        return 'Node: <%s:%s>' % (self.id, self.baptism_name)


@login_manager.user_loader
def load_user(user_id):
    return Node.query.get(int(user_id))


Relations = {
    'directed_types': {
        3: ['parent', 4], 4: ['child', 3]},
    'undirected_types': {
        1: ['partner'], 2: ['sibling', 3]},
    'all_types': {
        1: 'partner', 2: 'sibling', 3: 'parent',
        4: 'child', 5: 'nibling', 6: 'uncle-aunt'}
}


class GlobalGraph:

    def __init__(self, app):
        self.gpickle_path = app.config['GRAPH_PATH']
        self.authorised = False
        if app.config['TESTING'] is True or app.config['DEBUG'] is True:
            self.authorised = True

    def update(self):
        G = self.current
        relation_links = GlobalEdge.query.all()
        for link in relation_links:
            source = link.ascendant_id
            target = link.descendant_id
            weight = link.edge_label
            key = link.ascendant_id
            if not G.has_edge(source, target, key=key):
                G.add_edge(source, target, key=key, weight=weight)
        self.save(G)

    def clear(self):
        if self.authorised:
            G = self.current
            G.clear()
            self.save(G)

    @property
    def current(self):
        return self._load()

    def save(self, G):
        nx.write_gpickle(G, self.gpickle_path)

    def _load(self):
        if os.path.exists(self.gpickle_path):
            G = nx.read_gpickle(self.gpickle_path)
        else:
            G = nx.MultiDiGraph()
        return G


class Seed(Command):
    """Create fake seed data and store in database"""
    # This function should be protected

    @classmethod
    def run(cls):
        if current_app.config['DEBUG'] or current_app.config['TESTING']:
            a1 = Node(baptism_name='Chris', email='chris@test.com')
            a2 = Node(baptism_name='Christine', email='christine@test.com')
            a3 = Node(baptism_name='Charlie', email='charles@test.com')
            a4 = Node(baptism_name='Carol', email='carol@test.com')
            result = cls.relate(parents=[a1, a2], children=[a3, a4])
        return result

    @classmethod
    def relate(cls, partners=None, parents=None, children=None):
        result_dict = {}
        if current_app.config['DEBUG'] or current_app.config['TESTING']:
            if partners and not parents and not children:
                result_dict['nodes'] = cls._commit_nodes_to_db(
                    partners=partners)
                links = cls._links_constructor(partners=partners)
            elif parents and children and not partners:
                result_dict['nodes'] = cls._commit_nodes_to_db(
                    parents=parents,
                    children=children)
                links = cls._links_constructor(parents=parents,
                                               children=children)
            else:
                raise Exception('Expects: (**partners)/(**parents,**children)')
        result_dict['links'] = cls.connect_links(links)
        db.session.commit()
        return result_dict

    @classmethod
    def connect_links(cls, links):
        _processed_list = []
        for link in links:
            asc = links[link][0]
            descedants = links[link][1:-1]
            weight = links[link][-1]
            for des in descedants:
                (created_edge, created_status) = cls._get_or_create_one(
                    session=db.session,
                    model=GlobalEdge,
                    create_method='safe',
                    ascendant=asc,
                    descendant=des,
                    edge_label=weight)
                if created_status is True:
                    _processed_list.append(created_edge)
        return _processed_list

    @classmethod
    def _commit_nodes_to_db(cls, **kwargs):
        _processed_list = []
        for node_type in kwargs:
            for node in kwargs[node_type]:
                (created_node, created_status) = cls._get_or_create_one(
                    session=db.session,
                    model=Node,
                    create_method='auto',
                    create_method_kwargs={'node': node},
                    baptism_name=node.baptism_name)
                if created_status is True:
                    _processed_list.append(created_node)
        return _processed_list

    @staticmethod
    def _get_or_create_one(session, model, create_method='',
                           create_method_kwargs=None, **kwargs):
        try:
            return session.query(model).filter_by(**kwargs).one(), False
        except NoResultFound:
            kwargs.update(create_method_kwargs or {})
            created = getattr(model, create_method, model)(**kwargs)
            if created is not None:
                try:
                    session.add(created)
                    session.flush()
                    return created, True
                except IntegrityError:
                    session.rollback()
                    return session.query(model).filter_by(**kwargs).one(),
                    False
            else:
                return None, False

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
