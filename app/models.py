from . import db
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_script import Command
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
	relation_dict = {
		1:'partner',
		2:'sibling',
		3:'parent',
		4:'child',
		5:'nibling',
		6:'uncle-aunt'
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

	def get_relation_to(self, target):
		weight_list=[]
		relation_list=[]
		computed_path_list = self._node_path_list_to(target)
		computed_path_lengths = self._node_path_lengths(target)
		self.path = computed_path_list
		if self.path:
			for node in self.path:
				if node in computed_path_lengths:
					weight_list.append(computed_path_lengths[node])
			for weight in weight_list:
				if weight in self.relation_dict:
					relation_list.append(self.relation_dict[weight])
			self.relation_type = (relation_list, weight_list, computed_path_lengths, computed_path_list)
		return self

	def _dijkstra_paths_and_lengths_to(self, target):
		G = self.graph_output
		_length, _path = nx.single_source_dijkstra(G, self, target=target, weight='label')
		return (_length, _path)

	def _node_path_list_to(self, target):
		try:
			path_list = self._dijkstra_paths_and_lengths_to(target)[1]
			return path_list[target]
		except KeyError:
			# print("node %s not reachable from %s" % (source, target))
			return None

	def _node_path_lengths(self, target):
		try:
			lengths = self._dijkstra_paths_and_lengths_to(target)[0]
			return lengths
		except KeyError:
			# print("node %s not reachable from %s" % (source, target))
			return None

	def _create_graph(self, gtype=nx.Graph):
		_graph_output = gtype()
		db_paths = db.session.query(GlobalEdge).filter(GlobalEdge.descendant!=self).all()
		for edge in db_paths:
			n1 = edge.descendant
			n2 = edge.ascendant
			label = edge.edge_label
			_graph_output.add_edges_from([(n1,n2,{'label':label})])
		return (self, _graph_output)

	# This function should be protected
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

	@property
	def current(self):
		return self._load()

	def _save(self, G):
		nx.write_gpickle(G, current_app.config['GRAPH_PATH'])

	def _load(self):
		if os.path.exists(current_app.config['GRAPH_PATH']):
			G = nx.read_gpickle(current_app.config['GRAPH_PATH'])
		else:
			G = nx.MultiDiGraph()
		return G

class Seed(Command):
	"""Create fake seed data and store in database"""
	# This function should be protected
	@staticmethod
	def run():
		if current_app.config['DEBUG'] or current_app.config['TESTING']:
			n1 = Node(baptism_name='Chris', email='chris@family.com', dob=date(1900,11,1))
			n2 = Node(baptism_name='Christine', email='christine@family.com', dob=date(1910,12,2))
			n3 = Node(baptism_name='Charlie', email='charlie@family.com', dob=date(1925,10,3))
			n4 = Node(baptism_name='Carol', email='carol@family.com', dob=date(1930,8,4))
			links = {
				1: [n1,n2,1],
				2: [n1,n3,3],
				3: [n1,n4,3],
				4: [n2,n3,3],
				5: [n2,n4,3],
				6: [n3,n4,2]
			}
			db.session.add_all([n1,n2,n3,n4])
			result = Node.seed_node_family(links)
			return result
		return None

	@staticmethod
	def link_new_member(*args, **kwargs):
		if current_app.config['DEBUG']  or current_app.config['TESTING']:
			if kwargs['type']=='daughter':
				links = {
					1:[args[0],args[4],3],
					2:[args[1],args[4],3],
					3:[args[2],args[4],2],
					4:[args[3],args[4],2]
				}
				db.session.add(args[4])
				Node.seed_node_family(links)
			elif kwargs['type']=='wife':
				link = {
					1:[args[0],args[1],1]
				}
				db.session.add(args[1])
				Node.seed_node_family(link)
			elif kwargs['type']=='child':
				links = {
					1:[args[0],args[2],3],
					2:[args[1],args[2],3]
				}
				db.session.add_all([args[1],args[2]])
				Node.seed_node_family(links)

	@staticmethod
	def count_edge_labels(**kwargs):
		data = kwargs['data']
		counts={}
		for index,edge in enumerate(data):
			if counts.get(data[index][2]['label']):
				counts[data[index][2]['label']]=counts[data[index][2]['label']]+1
			else:
				counts[data[index][2]['label']]=1
		return counts