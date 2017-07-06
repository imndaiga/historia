from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import date
from . import db, graph


class Link(db.Model):
    '''Sqlalchemy model for a single-edge relationship between two persons'''
    __tablename__ = 'links'

    ancestor_id = db.Column(
        db.Integer,
        db.ForeignKey('persons.id', ondelete="CASCADE"),
        primary_key=True
    )
    descendant_id = db.Column(
        db.Integer,
        db.ForeignKey('persons.id', ondelete="CASCADE"),
        primary_key=True
    )
    weight = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Link %s-%s:%s>' % (
            self.ancestor_id,
            self.descendant_id,
            self.weight
        )


class Person(db.Model):
    '''An sqlalchemy person model'''
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    ethnic_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(64))
    birth_date = db.Column(db.DateTime, default=date(9999, 1, 1))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    descendants = db.relationship(
        'Link',
        foreign_keys=[Link.ancestor_id],
        backref=db.backref('ancestor', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    ancestors = db.relationship(
        'Link',
        foreign_keys=[Link.descendant_id],
        backref=db.backref('descendant', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def get_or_create_relationship(self, target, weight):
        '''
        Creates a relationship (two complementary links) between
        instance and target Person.
        it 'heals' the Link table if one or more link(s) are not found.
        '''
        link1, link1_exists = get_one_or_create(
            session=db.session,
            model=Link,
            ancestor_id=self.id,
            descendant_id=target.id,
            weight=weight
        )
        link2, link2_exists = get_one_or_create(
            session=db.session,
            model=Link,
            ancestor_id=target.id,
            descendant_id=self.id,
            weight=Relations.get_inverse_weight(weight)
        )

        db.session.commit()
        relationship = [link1, link2]

        graph.add_relationship(relationship)

        return relationship, link1_exists and link2_exists

    def get_graph(self):
        return graph.get_subgraph_from_person(self)

    @classmethod
    def create_from_email(cls, **kwargs):
        first_name = kwargs.get('first_name', None)
        ethnic_name = kwargs.get('ethnic_name', None)
        last_name = kwargs.get('last_name', None)
        sex = kwargs.get('sex', None)
        birth_date = kwargs.get('birth_date', date(9999, 1, 1))
        email = kwargs.get('email', None)
        confirmed = False
        if email:
            return cls(first_name=first_name,
                       ethnic_name=ethnic_name,
                       last_name=last_name,
                       sex=sex,
                       birth_date=birth_date,
                       email=email,
                       confirmed=confirmed)

    def __repr__(self):
        return 'Person: <%s:%s>' % (self.id, self.first_name)


class Relations:
    '''A model of weighted relations and labels'''

    all_types = {
        1: 'Partner', 2: 'Sibling', 3: 'Parent',
        4: 'Child', 5: 'Niece-Nephew', 6: 'Uncle-Aunt'
    }
    undirected_types = [1, 2]
    directed_types = [3, 4]
    modifiers = ['Great', 'Grand', 'In-law']

    @staticmethod
    def get_inverse_weight(weight):
        weight_pairings = [
            {1: 1},
            {2: 2},
            {3: 4},
            {4: 3}
        ]
        for pair in weight_pairings:
            for key, value in pair.items():
                if key == weight:
                    return value
        return None


def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    # reference: http://skien.cc/blog/2014/01/15/
    # sqlalchemy-and-race-conditions-implementing/
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, False
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True
