from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask_script import Command
from .models import Node, GlobalEdge
from .graph import GlobalGraph
from app import db


class Seed(Command):
    """Create fake seed data and store in database"""
    # This function should be protected

    def __init__(self, app, auto=False):
        self.app = app
        self.auto = auto
        self.graph = GlobalGraph(app)
        if self.app.config['DEBUG'] or self.app.config['TESTING']:
            self.authorised = True

    def run(self):
        if self.authorised is True:
            a1 = Node(baptism_name='Chris', email='chris@test.com')
            a2 = Node(baptism_name='Christine', email='christine@test.com')
            a3 = Node(baptism_name='Charlie', email='charles@test.com')
            a4 = Node(baptism_name='Carol', email='carol@test.com')
            result = self.relate(parents=[a1, a2], children=[a3, a4])
        self._graph_update(self.auto)
        return result

    def relate(self, partners=None, parents=None, children=None):
        result_dict = {}
        if self.authorised is True:
            if partners and not parents and not children:
                result_dict['nodes'] = self._commit_nodes_to_db(
                    partners=partners)
                links = self._links_constructor(partners=partners)
            elif parents and children and not partners:
                result_dict['nodes'] = self._commit_nodes_to_db(
                    parents=parents,
                    children=children)
                links = self._links_constructor(parents=parents,
                                                children=children)
            else:
                raise Exception('Expects: (**partners)/(**parents,**children)')
        result_dict['links'] = self._connect_links(links)
        db.session.commit()
        self._graph_update(self.auto)
        return result_dict

    def _graph_update(self, auto_flag):
        if auto_flag is True:
            self.graph.update()

    @classmethod
    def _connect_links(cls, links):
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
