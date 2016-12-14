from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager


Relations = {
    'directed_types': {
        3: ['parent', 4], 4: ['child', 3]},
    'undirected_types': {
        1: ['partner'], 2: ['sibling', 3]},
    'all_types': {
        1: 'partner', 2: 'sibling', 3: 'parent',
        4: 'child', 5: 'nibling', 6: 'uncle-aunt'}
}


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
            if link_label in Relations['directed_types'] or \
               link_label in Relations['undirected_types']:
                return cls(ascendant=ascendant,
                           descendant=descendant,
                           link_label=link_label)
        return None

    def __repr__(self):
        return '<Link %s-%s:%s>' % (self.ascendant_id,
                                    self.descendant_id,
                                    self.link_label)


class Person(db.Model, UserMixin):
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

    def auto(person, baptism_name):
        return person

    @staticmethod
    def person_from_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return {'sig': False, 'person': None}
        if data.get('email'):
            return {'sig': True, 'person': Person.query.filter_by(
                email=data.get('email')).first()}
        else:
            return {'sig': False, 'person': None}

    def __repr__(self):
        return 'Person: <%s:%s>' % (self.id, self.baptism_name)


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))
