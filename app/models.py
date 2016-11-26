from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager
import networkx as nx
import os

class GlobalEdge(db.Model):
	"""self-referential association table that connects Nodes"""
	__tablename__ = 'edges'

	def __init__(self, edge_label, **kwargs):
		super(GlobalEdge, self).__init__(**kwargs)
		self.edge_label = edge_label

	ascendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	edge_label = db.Column(db.Integer, default=0)

	def __repr__(self):
		return '<GlobalEdge %s-%s:%s>' % (self.ascendant_id, self.descendant_id, self.edge_label)

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
	descended_by = db.relationship('GlobalEdge',
								foreign_keys=[GlobalEdge.ascendant_id],
								backref=db.backref('ascendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	ascended_by = db.relationship('GlobalEdge',
								foreign_keys=[GlobalEdge.descendant_id],
								backref=db.backref('descendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	directed_types = { 3:['parent',4], 4:['child',3]}
	undirected_types = { 1:['partner'], 2:['sibling',3]}

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
		result_dict = {}

		if self.baptism_name != node.baptism_name:
			if label in self.directed_types:
				dir1 = GlobalEdge.query.filter_by(ascendant_id=self.id).filter_by(descendant_id=node.id).first()
				dir2 = GlobalEdge.query.filter_by(ascendant_id=node.id).filter_by(descendant_id=self.id).first()
				if not dir1 and not dir2:
					e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=label)
					e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=self.directed_types[label][1])
					db.session.add_all([e1,e2])
					db.session.commit()
					result_dict=GlobalGraph().update(edge_list=[e1,e2])
				elif dir1 and not dir2:
					e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=self.directed_types[label][1])
					db.session.add(e2)
					db.session.commit()
					result_dict=GlobalGraph().update(edge_list=[e2])
				elif not dir1 and dir2:
					e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=label)
					db.session.add(e1)
					db.session.commit()
					result_dict=GlobalGraph().update(edge_list=[e1])
				else:
					return None
			elif label in self.undirected_types:
				e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=label)
				e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=label)
				db.session.add_all([e1,e2])
				db.session.commit()
				result_dict=GlobalGraph().update(edge_list=[e1,e2])
			else:
				return None
			return result_dict
		else:
			return None

	def node_relation(self, target_node):
		G = self.graph_output
		try:
			self.path_nodes_list = nx.dijkstra_path(G, source=self, target=target_node, weight='label')
		except nx.NetworkXNoPath as e:
			# No relation between self and target_node
			self.path_nodes_list = None
			self.computed_relation_name = None
		return self

	def _create_graph(self, gtype=nx.Graph):
		_graph_output = gtype()
		db_paths = db.session.query(GlobalEdge).filter(GlobalEdge.descendant!=self).all()
		for edge in db_paths:
			n1 = edge.descendant
			n2 = edge.ascendant
			label = edge.edge_label
			_graph_output.add_edges_from([(n1,n2,{'label':label})])
		return (self, _graph_output)

	# This function should be password protected or hidden
	def _change_edge_label(self, node, edge_label):
		if self.baptism_name != node.baptism_name:
			if self.edge_ascends(node):
				n = GlobalEdge.query.filter_by(descendant_id=node.id).first()
			elif self.edge_descends(node):
				n = GlobalEdge.query.filter_by(ascendant_id=node.id).first()
			else:
				# Self and Node are not related, no edge_label change can be made
				return None
			n.edge_label = edge_label
			db.session.add(n)
			return n
		return None

	@property
	def graph_output(self):
		return self._create_graph()[1]

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
			result=links[link][0].create_edge(links[link][1], label=links[link][2])
		db.session.commit()
		return result

	@login_manager.user_loader
	def load_user(user_id):
		return Node.query.get(int(user_id))
					
	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name

class GlobalGraph:

	def update(self, edge_list):
		G = self._load()
		for edge in edge_list:
			source = edge.ascendant.id
			target = edge.descendant.id
			length = edge.edge_label
			G.add_edge(source, target, weight=length)
		self._save(G)
		return {'input':edge_list,'output':G}

	def _save(self, G):
		nx.write_gpickle(G, current_app.config['GRAPH_PATH'])

	def _load(self):
		if os.path.exists(current_app.config['GRAPH_PATH']):
			G = nx.read_gpickle(current_app.config['GRAPH_PATH'])
		else:
			G = nx.MultiDiGraph()
		return G