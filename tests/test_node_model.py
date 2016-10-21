import unittest
from app import create_app, db
from app.models import Node, Edge
from datetime import date

class NodeModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

		n1 = Node(baptism_name='Chris', yob=date(1900,11,1))
		n2 = Node(baptism_name='Christine', yob=date(1910,12,2))
		n3 = Node(baptism_name='Charlie', yob=date(1925,10,3))
		n4 = Node(baptism_name='Carol', yob=date(1930,8,4))
		links = {
			1: [n1,n2,0],
			2: [n1,n3,1],
			3: [n1,n4,1],
			4: [n2,n3,1],
			5: [n2,n4,1],
			6: [n3,n4,0]
		}
		Node.commit_node_branch(links)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_node_count(self):
		self.assertTrue(Node.query.count() == 4)

	def test_edge_count(self):
		self.assertTrue(Edge.query.count() == 6)

	def test_valid_step_edges(self):
		(n1,n2,n3,n4) = Node.query.all()
		self.assertTrue(n1._is_step_ascendant_to(n3))
		self.assertTrue(n1._is_step_ascendant_to(n2))
		self.assertTrue(n1._is_step_ascendant_to(n4))
		self.assertTrue(n2._is_step_ascendant_to(n3))
		self.assertTrue(n2._is_step_ascendant_to(n4))
		self.assertTrue(n3._is_step_ascendant_to(n4))
		

	def test_invalid_step_edges(self):
		(n1,n2,n3,n4) = Node.query.all()
		self.assertFalse(n1._is_step_descendant_to(n3))
		self.assertFalse(n1._is_step_descendant_to(n2))
		self.assertFalse(n1._is_step_descendant_to(n4))
		self.assertFalse(n2._is_step_descendant_to(n3))
		self.assertFalse(n2._is_step_descendant_to(n4))
		self.assertFalse(n3._is_step_descendant_to(n4))

	def test_change_step_edge_weights(self):
		(n1,n2,n3,n4) = Node.query.all()
		n5 = Node(baptism_name='Coraline',yob=date(1940,7,5))
		db.session.add(n5)
		db.session.commit()
		self.assertFalse(n5.change_step_edge_weight(n1,1))
		self.assertFalse(n5.change_step_edge_weight(n2,1))
		self.assertFalse(n5.change_step_edge_weight(n3,0))
		self.assertFalse(n5.change_step_edge_weight(n4,0))
		links = {
			1:[n1,n5,1],
			2:[n2,n5,1],
			3:[n3,n5,0],
			4:[n4,n5,0]
		}
		n5.commit_node_branch(links)
		self.assertTrue(n5.change_step_edge_weight(n1,1))
		self.assertTrue(n5.change_step_edge_weight(n2,1))
		self.assertTrue(n5.change_step_edge_weight(n3,0))
		self.assertTrue(n5.change_step_edge_weight(n4,0))


	def test_invalid_self_edge(self):
		n1 = Node.query.get(1)
		self.assertFalse(n1.create_step_edge(n1,1))
		self.assertFalse(n1.change_step_edge_weight(n1,1))