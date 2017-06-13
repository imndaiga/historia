from . import db, graph
from datetime import date


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

    @classmethod
    def safe(cls, ancestor, descendant, weight):
        if ancestor != descendant:
            if weight in graph.Relations['directed_types'] or \
               weight in graph.Relations['undirected_types']:
                return cls(
                    ancestor=ancestor,
                    descendant=descendant,
                    weight=weight
                )
        return None

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
            return None

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
            db.session.add_all([link_1, link_2])
            db.session.commit()
        else:
            return relation

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
    def auto(cls, email=None, person=None):
        if person is None and email is not None:
            return cls(email=email)
        elif person is not None and email is not None:
            return person

    def __repr__(self):
        return 'Person: <%s:%s>' % (self.id, self.first_name)
