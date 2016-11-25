from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import login_manager
import networkx as nx

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

	directed_types = {
		'parent-child':[3,4],
		'uncle_aunt-nibling':[6,5]
		}

	undirected_types = {
		'siblings':2,
		'partners':1
	}

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
			dir_type_list = []

			for l in list(self.directed_types.values()):
				dir_type_list.extend(l)

			if label in dir_type_list:
				for relation in self.directed_types:
					if label in self.directed_types[relation]:
						dir1 = GlobalEdge.query.filter_by(ascendant_id=self.id).filter_by(descendant_id=node.id).first()
						dir2 = GlobalEdge.query.filter_by(ascendant_id=node.id).filter_by(descendant_id=self.id).first()
						if not dir1 and not dir2:
							e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=self.directed_types[relation][0])
							e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=self.directed_types[relation][1])
							db.session.add_all([e1,e2])
							db.session.commit()
							result_dict=GlobalGraph(edge_list=[e1,e2]).add()
						elif dir1 and not dir2:
							e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=self.directed_types[relation][1])
							db.session.add(e2)
							result_dict=GlobalGraph(edge_list=[e2]).add()
						elif not dir1 and dir2:
							e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=self.directed_types[relation][0])
							db.session.add(e1)
							listed_tuple=(e1)
							result_dict=GlobalGraph(edge_list=[e1]).add()
						else:
							return None
			elif label in list(self.undirected_types.values()):
				for relation in self.undirected_types:
					if label == self.undirected_types[relation]:
						e1 = GlobalEdge(ascendant=self, descendant=node, edge_label=label)
						e2 = GlobalEdge(ascendant=node, descendant=self, edge_label=label)
						db.session.add_all([e1,e2])
						result_dict=GlobalGraph(edge_list=[e1,e2]).add()
			else:
				return None
			return result_dict
		return None

	def node_relation(self, target_node):
		G = self.graph_output
		try:
			self.get_path = nx.dijkstra_path(G, source=self, target=target_node, weight='label')
		except nx.NetworkXNoPath as e:
			self.get_path = None
			self.get_type = None
			print('No relation between {} and {}.'.format(self, target_node))
			return None
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
	def __init__(self, **kwargs):
		self.edge_list = kwargs['edge_list']

	def add(self):
		# should read graph from database
		G = nx.MultiDiGraph()

		for index,edge in enumerate(self.edge_list):
			self.source = self.edge_list[index].ascendant
			self.target = self.edge_list[index].descendant
			self.length = self.edge_list[index].edge_label
			G.add_edge(self.source, self.target, weight=self.length)

		return {'input':self.edge_list,'output':G}