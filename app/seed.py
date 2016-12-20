from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask_script import Command


class Seed(Command):
    """Create fake seed data and store in database"""
    # This function should be protected

    auto = False
    authorised = False

    def init_app(self, app, auto):
        from app.models import Person, Link
        from app import db, graph
        self.Person = Person
        self.Link = Link
        self.db = db
        self.graph = graph
        self.auto = auto
        if app.config['DEBUG'] or app.config['TESTING']:
            self.testing = True

    def run(self):
        if self.testing is True:
            a1 = self.Person(baptism_name='Chris', email='chris@test.com')
            a2 = self.Person(
                baptism_name='Christine',
                email='christine@test.com')
            a3 = self.Person(baptism_name='Charlie', email='charles@test.com')
            a4 = self.Person(baptism_name='Carol', email='carol@test.com')
            result = self.relate(parents=[a1, a2], children=[a3, a4])
        self._graph_update(self.auto)
        return result

    def relate(self, partners=None, parents=None, children=None):
        result_dict = {}
        if self.testing is True:
            if partners and not parents and not children:
                result_dict['persons'] = self._commit_persons_to_db(
                    partners=partners)
                relations = self._relations_constructor(partners=partners)
            elif parents and children and not partners:
                result_dict['persons'] = self._commit_persons_to_db(
                    parents=parents,
                    children=children)
                relations = self._relations_constructor(parents=parents,
                                                        children=children)
            else:
                raise Exception('Expects: (**partners)/(**parents,**children)')
        result_dict['relations'] = self._connect_relations(relations)
        self.db.session.commit()
        self._graph_update(self.auto)
        return result_dict

    def _graph_update(self, auto_flag):
        if auto_flag is True:
            self.graph.update()

    def _connect_relations(self, relations):
        _processed_list = []
        for relation in relations:
            asc = relations[relation][0]
            descedants = relations[relation][1:-1]
            weight = relations[relation][-1]
            for des in descedants:
                (created_link, created_status) = self._get_or_create_one(
                    session=self.db.session,
                    model=self.Link,
                    create_method='safe',
                    ascendant=asc,
                    descendant=des,
                    link_label=weight)
                if created_status is True:
                    _processed_list.append(created_link)
        return _processed_list

    def _commit_persons_to_db(self, **kwargs):
        _processed_list = []
        for person_type in kwargs:
            for person in kwargs[person_type]:
                (created_person, created_status) = self._get_or_create_one(
                    session=self.db.session,
                    model=self.Person,
                    create_method='auto',
                    create_method_kwargs={'person': person},
                    baptism_name=person.baptism_name)
                if created_status is True:
                    _processed_list.append(created_person)
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
    def _post_process_relations(preprocessed):
        ret_dict = {}
        _inverse = {}

        if 2 in preprocessed and \
           1 in preprocessed and \
           0 not in preprocessed:

            for i, parent_person in enumerate(preprocessed[1]):
                index = i + 1
                ret_dict[index] = [[parent_person], preprocessed[2], [3]]
                next_index = index + 1
            index = next_index
            for child_person in preprocessed[2]:
                ret_dict[index] = [[child_person], preprocessed[1], [4]]
                index += 1
                next_index = index
            index = next_index

            if len(preprocessed[1]) > 1:
                # ensure self-loop relations are not constructed
                for current_index, partner_person in enumerate(
                        preprocessed[1]):
                    _inverse['self'] = preprocessed[1].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[partner_person], _inverse['self'], [1]]
                    _inverse.clear()
                    index += 1
                    next_index = index
                index = next_index
            if len(preprocessed[2]) > 1:
                # ensure self-loop relations are not constructed
                for current_index, sibling_person in enumerate(
                        preprocessed[2]):
                    _inverse['self'] = preprocessed[2].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[sibling_person], _inverse['self'], [2]]
                    _inverse.clear()
                    index += 1
        elif 0 in preprocessed and \
                2 not in preprocessed and \
                1 not in preprocessed:

            if len(preprocessed[0]) > 1:
                # ensure self-loop relations are not constructed
                index = 1
                for current_index, partner_person in enumerate(
                        preprocessed[0]):
                    _inverse['self'] = preprocessed[0].copy()
                    _inverse['self'].pop(current_index)
                    ret_dict[index] = [[partner_person], _inverse['self'], [1]]
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
    def _relations_constructor(cls, **kwargs):
        _process_dict = {}
        for person_type in kwargs:
            if person_type == 'parents':
                _process_dict[1] = kwargs[person_type]
            elif person_type == 'partners':
                _process_dict[0] = kwargs[person_type]
            elif person_type == 'children':
                _process_dict[2] = kwargs[person_type]

        constructed_relation_dict = cls._post_process_relations(_process_dict)
        return constructed_relation_dict
