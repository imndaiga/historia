from . import db, graph
from datetime import date


class Link(db.Model):
    """self-referential association table that connects Nodes"""
    __tablename__ = 'links'

    ascendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
                             primary_key=True)
    descendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
                              primary_key=True)
    link_label = db.Column(db.Integer, default=0)

    @classmethod
    def safe(cls, ascendant, descendant, link_label):
        if ascendant != descendant:
            if link_label in graph.Relations['directed_types'] or \
               link_label in graph.Relations['undirected_types']:
                return cls(ascendant=ascendant,
                           descendant=descendant,
                           link_label=link_label)
        return None

    def __repr__(self):
        return '<Link %s-%s:%s>' % (self.ascendant_id,
                                    self.descendant_id,
                                    self.link_label)


class Person(db.Model):
    """all miminani subscribed Nodes"""
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    baptism_name = db.Column(db.String(64))
    ethnic_name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(64))
    dob = db.Column(db.DateTime, default=date(9999, 1, 1))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    descended_by = db.relationship('Link',
                                   foreign_keys=[Link.ascendant_id],
                                   backref=db.backref(
                                       'ascendant', lazy='joined'),
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    ascended_by = db.relationship('Link',
                                  foreign_keys=[Link.descendant_id],
                                  backref=db.backref(
                                      'descendant', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')

    def link_ascends(self, person):
        return self.descended_by.filter_by(
            descendant_id=person.id).first() is not None

    def link_descends(self, person):
        return self.ascended_by.filter_by(
            ascendant_id=person.id).first() is not None

    # This function should be protected
    def _change_link_label(self, person, link_label):
        if self.baptism_name != person.baptism_name:
            if self.link_ascends(person):
                retrieved_link = Link.query.filter_by(
                    descendant_id=person.id).first()
            elif self.link_descends(person):
                retrieved_link = Link.query.filter_by(
                    ascendant_id=person.id).first()
            else:
                # Self and Person are not related, no link_label change can be
                # made
                return None
            retrieved_link.link_label = link_label
            db.session.add(retrieved_link)
            return retrieved_link
        return None

    @classmethod
    def auto(cls, email=None, person=None):
        if person is None and email is not None:
            return cls(email=email)
        elif person is not None and email is not None:
            return person

    def __repr__(self):
        return 'Person: <%s:%s>' % (self.id, self.baptism_name)
