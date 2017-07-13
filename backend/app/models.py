from datetime import date
from . import db, graph
from .utils import get_one_or_create, Relations


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

        graph.create_from_model_instance(link1)
        graph.create_from_model_instance(link2)

        return [link1, link2], link1_exists and link2_exists

    def get_graph(self):
        return graph.get_subgraph_from_id(self.id)

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
