from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager
import networkx as nx
from sqlalchemy import or_

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
	edge_label = db.Column(db.Integer, default=0)

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
		label_check = 0

		directed_types = {
		'parent-child':[3,4],
		'uncle_aunt-nibling':[6,5]
		}

		undirected_types = {
			'siblings':2,
			'partners':1
		}

		if self.baptism_name != node.baptism_name:
			dir_type_list = []
			for l in list(directed_types.values()):
				dir_type_list.extend(l)
			if label in dir_type_list:
				for relation in directed_types:
					if label in directed_types[relation]:
						dir1 = Edge.query.filter_by(ascendant_id=self.id).filter_by(descendant_id=node.id).first()
						dir2 = Edge.query.filter_by(ascendant_id=node.id).filter_by(descendant_id=self.id).first()
						if not dir1 and not dir2:
							n1 = Edge(ascendant=self, descendant=node, edge_label=directed_types[relation][0])
							n2 = Edge(ascendant=node, descendant=self, edge_label=directed_types[relation][1])
							db.session.add_all([n1,n2])
							label_check = 3
						elif dir1 and not dir2:
							n2 = Edge(ascendant=node, descendant=self, edge_label=directed_types[relation][1])
							db.session.add(n2)
							label_check = 2
						elif not dir1 and dir2:
							n1 = Edge(ascendant=self, descendant=node, edge_label=directed_types[relation][0])
							db.session.add(n1)
							label_check = 1
						else:
							return None
			elif label in list(undirected_types.values()):
				for relation in undirected_types:
					if label == undirected_types[relation]:
						n = Edge(ascendant=self, descendant=node, edge_label=label)
						db.session.add(n)
			else:
				return None
			return (self,node,label_check)
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
		result = []
		for link in links:
			result.append(links[link][0].create_edge(links[link][1], label=links[link][2]))
		db.session.commit()
		return result

	@login_manager.user_loader
	def load_user(user_id):
		return Node.query.get(int(user_id))
					
	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name

class Graph():
	def __init__(self, node, **kwargs):
		if isinstance(node, Node):
			self.node = node
			self.valid = True
		else:
			self.node = node
			self.valid = False

	def create(self, gtype=nx.Graph):
		if self.valid:
			self.nodegraph = gtype()
			db_paths = db.session.query(Edge).filter(or_(Edge.descendant==self.node, Edge.ascendant==self.node)).all()
			for edge in db_paths:
				n1 = edge.descendant
				n2 = edge.ascendant
				label = edge.edge_label
				self.nodegraph.add_nodes_from([n1,n2])
				self.nodegraph.add_edges_from([(n1,n2,{'label':label})])
		else:
			raise TypeError('{} is of type {}. Node type is expected.'.format(self.node, type(self.node)))			
		return self.nodegraph