from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Edge(db.Model):
	"""self-referential association table that connects Nodes"""
	__tablename__ = 'Edges'
	ascendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	edge_weight = db.Column(db.Integer)

	def __repr__(self):
		return '<Edge %s-%s:%s>' % (self.ascendant_id, self.descendant_id, self.edge_weight)

class Node(db.Model):
	"""all miminani subscribed Nodes"""
	__tablename__ = 'nodes'
	id = db.Column(db.Integer, primary_key=True)
	baptism_name = db.Column(db.String(64))
	ethnic_name = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	sex = db.Column(db.String(64))
	dob = db.Column(db.DateTime, default=date(9999,1,1))
	email = db.Column(db.String(64), unique=True)
	confirmed = db.Column(db.Boolean, default=False)

	descended_by = db.relationship('Edge',
								foreign_keys=[Edge.ascendant_id],
								backref=db.backref('ascendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	ascended_by = db.relationship('Edge',
								foreign_keys=[Edge.descendant_id],
								backref=db.backref('descendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	def generate_login_token(self, remember_me=False, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'login': self.id, 'remember_me': remember_me})

	def generate_confirmation_and_login_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id, 'login': self.id, 'remember_me': False})

	def confirm_login(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('login') != self.id:
			return False
		return {'remember_me': data.get('remember_me')}

	def confirm_email(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def create_edge(self, node, edge_weight):
		if self.baptism_name != node.baptism_name:
			if node.dob > self.dob:
				if not self._is_edge_ascendant_to(node):
					n = Edge(ascendant=self, descendant=node, edge_weight=edge_weight)
					db.session.add(n)
					return self
			else:
				if not node._is_edge_ascendant_to(self):
					n = Edge(ascendant=node, descendant=self, edge_weight=edge_weight)
					db.session.add(n)
					return node
		return None

	def change_edge_weight(self, node, edge_weight):
		if self.baptism_name != node.baptism_name:
			if self._is_edge_ascendant_to(node):
				n = Edge.query.filter_by(descendant_id=node.id).first()
			elif self._is_edge_descendant_to(node):
				n = Edge.query.filter_by(ascendant_id=node.id).first()
			else:
				# Self and Node are not related, no edge_weight change can be made
				return None
			n.edge_weight = edge_weight
			db.session.add(n)
			return n
		return None

	@staticmethod
	def seed_node_family(links=None):
		if links:
			for link in links:
				db.session.add_all([links[link][0],links[link][1]])
				db.session.commit()
				links[link][0].create_edge(links[link][1], edge_weight=links[link][2])
			return links
		else:
			return None

	def _is_edge_ascendant_to(self, node):
		return self.descended_by.filter_by(
			descendant_id=node.id).first() is not None

	def _is_edge_descendant_to(self, node):
		return self.ascended_by.filter_by(
			ascendant_id=node.id).first() is not None
					
	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name