import unittest
from app import create_app, db
from app.models import Node, Edge

class NodeModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Node.commit_node_branch('testing')

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_node_count(self):
		self.assertTrue(Node.query.count() == 31)

	def test_edge_count(self):
		self.assertTrue(Edge.query.count() == 60)

	def test_valid_node_edges(self):
		n1 = Node(baptism_name='Chris')
		n2 = Node(baptism_name='Christine')
		n3 = Node(baptism_name='Charlie')
		n4 = Node(baptism_name='Carol')

		links = {
			1: [n1,n2,0],
			2: [n1,n3,1],
			3: [n1,n4,1],
			4: [n2,n3,1],
			5: [n2,n4,1],
			6: [n3,n4,0]
		}

		Node.commit_node_branch(links)
		
		self.assertTrue(n1.is_step_ascendant_to(n3))
		self.assertTrue(n1.is_step_ascendant_to(n2))
		self.assertTrue(n1.is_step_ascendant_to(n4))
		self.assertTrue(n2.is_step_ascendant_to(n3))
		self.assertTrue(n2.is_step_ascendant_to(n4))
		self.assertTrue(n3.is_step_ascendant_to(n4))
		self.assertFalse(n1.is_step_descendant_to(n3))
		self.assertFalse(n1.is_step_descendant_to(n2))
		self.assertFalse(n1.is_step_descendant_to(n4))
		self.assertFalse(n2.is_step_descendant_to(n3))
		self.assertFalse(n2.is_step_descendant_to(n4))
		self.assertFalse(n3.is_step_descendant_to(n4))