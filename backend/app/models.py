from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import date
from . import db


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


class LinkError(Exception):
    '''Basic exception for errors raised by relational inconsistencies'''

    def __init__(self, msg=None):
        if msg is None:
            msg = 'An link error occured involving'
        super(LinkError, self).__init__(msg)


class LinkMissingError(LinkError):
    '''Raised when a two-way relation is missing a link'''

    def __init__(self, available_link):
        super(LinkMissingError, self).__init__(
            msg='Complementary link to %s missing' % available_link)


class RelationInvalidError(LinkError):
    '''Raised when a relation composed of 2 links is invalid'''

    def __init__(self, error_links):
        super(RelationInvalidError, self).__init__(
            msg='Invalid relation found: [%s, %s]'
                % (error_links[0], error_links[1])
        )


class Link(db.Model):
    '''Sqlalchemy model for a single-edge relation between two persons'''
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

    def get_or_create_relation(self, target, weight):
        '''
        Tries to create a relation (two complementary links) between
        instance and target Person.
        If one already exists, it returns the relation.
        If a missing link from a relation pair is missing, it 'heals'
        the Link table.
        '''
        try:
            exists, relation = self.search_for_relation(target)
        except LinkMissingError as e:
            # Fix relation errors here
            print(e)
            return None, False

        if not exists:
            link_1 = Link(
                ancestor_id=self.id,
                descendant_id=target.id,
                weight=weight
            )
            link_2 = Link(
                ancestor_id=target.id,
                descendant_id=self.id,
                weight=get_inverse_weight(weight)
            )
            relation = [link_1, link_2]
            db.session.add_all(relation)
            db.session.flush()
            return relation, False
        else:
            return relation, True

    def search_for_relation(self, target):
        '''
        Search the Link table for paired records.
        Return a LinkMissingError if only one link is found.
        Otherwise, no relation exists.
        '''
        descendant_self = [
            d for d in target.descendants if d.descendant_id == self.id
        ]
        descendant_target = [
            a for a in target.ancestors if a.ancestor_id == self.id
        ]

        if descendant_self and descendant_target:
            return True, [descendant_target, descendant_self]
        elif descendant_self and not descendant_target:
            raise LinkMissingError(descendant_self)
        elif not descendant_self and descendant_target:
            raise LinkMissingError(descendant_target)
        else:
            return False, None

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
