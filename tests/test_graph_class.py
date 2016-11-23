import unittest
from app import create_app, db
from app.models import Node, Edge, Graph
from datetime import date
import networkx as nx

class GraphTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

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
		Node.seed_node_family(links)

	def tearDown(self):
		db.session.rollback()
		db.drop_all()
		self.app_context.pop()

	def test_invalid_graph_argument(self):
		n1 = Node.query.get(1)
		with self.assertRaises(TypeError):
			Graph('node').create()

	def test_valid_graph_argument(self):
		n1 = Node.query.get(1)
		self.assertTrue(isinstance(Graph(n1).create().output.nodes(), list))
		self.assertTrue(isinstance(Graph(n1).create().output.edges(), list))

	def test_count_digraph_elements(self):
		n1 = Node.query.get(1)
		self.assertTrue(Graph(n1).create().count().numedges==5)
		self.assertTrue(Graph(n1).create().count().numnodes==4)

	def test_count_undirgraph_elements(self):
		n1 = Node.query.get(1)
		self.assertTrue(Graph(n1).create(gtype=nx.Graph).count().numedges==3)
		self.assertTrue(Graph(n1).create(gtype=nx.Graph).count().numnodes==4)

		
