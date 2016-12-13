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


class GlobalEdge(db.Model):
    """self-referential association table that connects Nodes"""
    __tablename__ = 'edges'

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
