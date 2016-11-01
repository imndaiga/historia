from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager

class Edge(db.Model):
	"""self-referential association table that connects Nodes"""
	__tablename__ = 'edges'

	def __init__(self, edge_label, **kwargs):
		super(Edge, self).__init__(**kwargs)
		self.edge_label = edge_label

	ascendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	_edge_label = db.Column(db.Integer, default=0)

	directed_types = {
		'parent-child':[3,4],
		'uncle_aunt-nibling':[6,5]
	}

	undirected_types = {
		2:'siblings',
		1:'partners'
	}

	@classmethod
	def set_label(cls, asc, des, _edge_label):
		e = cls(ascendant=des, descendant=asc, edge_label=None)
		e._edge_label=_edge_label
		db.session.add(e)
	
	@property
	def edge_label(self):
		return self._edge_label

	@edge_label.setter
	def edge_label(self, label):
		for stype in self.directed_types:
			if label in self.directed_types[stype]:
				ascendant_tree = self.query.filter_by(ascendant=self.ascendant).filter_by(descendant=self.descendant).all()
				descendant_tree = self.query.filter_by(ascendant=self.descendant).filter_by(descendant=self.ascendant).all()
				if ascendant_tree and descendant_tree:
					return self
				elif not ascendant_tree and not descendant_tree:
					self._edge_label = self.directed_types[stype][0]
					Edge.set_label(self.ascendant,self.descendant,_edge_label=self.directed_types[stype][1])
				elif ascendant_tree and not descendant_tree:
					Edge.set_label(self.ascendant,self.descendant,_edge_label=self.directed_types[stype][1])
				elif not ascendant_tree and descendant_tree:
					self._edge_label = self.directed_types[stype][0]
			else:
				self._edge_label = label

	def __repr__(self):
		return '<Edge %s-%s:%s>' % (self.ascendant_id, self.descendant_id, self.edge_label)

class Node(db.Model, UserMixin):
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

	def generate_login_token(self, email, remember_me=False, next_url=None, expiration=300):
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
		return {'remember_me': data.get('remember_me'), 'next_url': data.get('next_url')}

	def edge_ascends(self, node):
		return self.descended_by.filter_by(
			descendant_id=node.id).first() is not None

	def edge_descends(self, node):
		return self.ascended_by.filter_by(
			ascendant_id=node.id).first() is not None

	def create_edge(self, node, label):
		if self.baptism_name != node.baptism_name:
			if node.dob > self.dob:
				if not self.edge_ascends(node):
					n = Edge(ascendant=self, descendant=node, edge_label=label)
					db.session.add(n)
					return self
			else:
				if not node.edge_ascends(self):
					n = Edge(ascendant=node, descendant=self, edge_label=label)
					db.session.add(n)
					return node
		return None

	# This function should be password protected or hidden
	def _change_edge_label(self, node, edge_label):
		if self.baptism_name != node.baptism_name:
			if self.edge_ascends(node):
				n = Edge.query.filter_by(descendant_id=node.id).first()
			elif self.edge_descends(node):
				n = Edge.query.filter_by(ascendant_id=node.id).first()
			else:
				# Self and Node are not related, no edge_label change can be made
				return None
			n.edge_label = edge_label
			db.session.add(n)
			return n
		return None
		
	@staticmethod
	def node_from_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return {'sig': False, 'node': None}
		if data.get('email'):
			return {'sig': True, 'node': Node.query.filter_by(email=data.get('email')).first()}
		else:
			return {'sig': False, 'node': None}

	@staticmethod
	def seed_node_family(links):
		for link in links:
			links[link][0].create_edge(links[link][1], label=links[link][2])
			db.session.commit()
		return links

	@login_manager.user_loader
	def load_user(user_id):
		return Node.query.get(int(user_id))
					
	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name