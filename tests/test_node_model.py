import unittest
from app import create_app, db
from app.models import Node, GlobalEdge, Seed
from datetime import date
import time
import networkx as nx

class NodeModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Seed.run()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_node_count(self):
		self.assertTrue(Node.query.count() == 4)

	def test_edge_count(self):
		self.assertTrue(GlobalEdge.query.count() == 12)

	def test_valid_edges(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		self.assertTrue(n1.edge_ascends(n3))
		self.assertTrue(n1.edge_ascends(n2))
		self.assertTrue(n1.edge_ascends(n4))
		self.assertTrue(n2.edge_ascends(n3))
		self.assertTrue(n2.edge_ascends(n4))
		self.assertTrue(n3.edge_ascends(n4))
		self.assertTrue(n1.edge_descends(n3))
		self.assertTrue(n1.edge_descends(n4))
		self.assertTrue(n2.edge_descends(n3))
		self.assertTrue(n2.edge_descends(n4))

	def test_valid_edge_addition(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		Seed.link_new_member(n1,n2,n3,n4,n5,type='daughter')
		self.assertTrue(GlobalEdge.query.count() == 20)

	def test_valid_label_change(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		Seed.link_new_member(n1,n2,n3,n4,n5,type='daughter')
		self.assertTrue(n5._change_edge_label(n1,1))
		self.assertTrue(n5._change_edge_label(n2,1))
		self.assertTrue(n5._change_edge_label(n3,0))
		self.assertTrue(n5._change_edge_label(n4,0))
		self.assertTrue(n1._change_edge_label(n5,1))
		self.assertTrue(n2._change_edge_label(n5,1))
		self.assertTrue(n3._change_edge_label(n5,0))
		self.assertTrue(n4._change_edge_label(n5,0))

	def test_invalid_label_change(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		db.session.add(n5)
		db.session.commit()
		self.assertFalse(n5._change_edge_label(n1,1))
		self.assertFalse(n5._change_edge_label(n2,1))
		self.assertFalse(n5._change_edge_label(n3,0))
		self.assertFalse(n5._change_edge_label(n4,0))
		self.assertFalse(n1._change_edge_label(n5,1))
		self.assertFalse(n2._change_edge_label(n5,1))
		self.assertFalse(n3._change_edge_label(n5,0))
		self.assertFalse(n4._change_edge_label(n5,0))

	def test_invalid_node_loop(self):
		n1 = Node.query.get(1)
		self.assertFalse(n1.create_edge(n1,1))
		self.assertFalse(n1._change_edge_label(n1,1))

	def test_valid_node_from_token(self):
		n1 = Node.query.get(1)
		token = n1.generate_login_token(email=n1.email)
		sig_data = Node.node_from_token(token)
		self.assertTrue(sig_data['node'].email == n1.email)

	def test_invalid_node_from_token(self):
		(n1,n2) = Node.query.slice(0,2)
		token = n1.generate_login_token(email=n1.email)
		sig_data = Node.node_from_token(token)
		self.assertFalse(sig_data['node'].email == n2.email)

	def test_expired_node_from_token(self):
		n1 = Node.query.get(1)
		token = n1.generate_login_token(email=n1.email, expiration=1)
		time.sleep(2)
		sig_data = Node.node_from_token(token)
		self.assertFalse(sig_data['sig'])

	def test_valid_login_token(self):
		n1 = Node.query.get(1)
		token = n1.generate_login_token(email=n1.email)
		self.assertTrue(n1.confirm_login(token))

	def test_invalid_login_token(self):
		(n1,n2) = Node.query.slice(0,2)
		token = n1.generate_login_token(email=n1.email)
		self.assertFalse(n2.confirm_login(token))

	def test_expired_login_token(self):
		n1 = Node.query.get(1)
		token = n1.generate_login_token(expiration=1, email=n1.email)
		time.sleep(2)
		self.assertFalse(n1.confirm_login(token))

	def test_valid_node_undirgraph_argument(self):
		n1 = Node.query.get(1)
		self.assertIsInstance(n1.graph_output.nodes(), list)
		self.assertIsInstance(n1.graph_output.edges(), list)

	def test_basic_undirgraph_count(self):
		n1 = Node.query.get(1)
		self.assertTrue(n1.graph_output.number_of_edges()==6)
		self.assertTrue(n1.graph_output.number_of_nodes()==4)

	def test_pre_existing_node_relations(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		self.assertIsInstance(n1.get_relation_to(n2).path, list)
		self.assertIsInstance(n1.get_relation_to(n3).path, list)
		self.assertIsInstance(n1.get_relation_to(n4).path, list)
		self.assertIsInstance(n2.get_relation_to(n1).path, list)
		self.assertIsInstance(n2.get_relation_to(n3).path, list)
		self.assertIsInstance(n2.get_relation_to(n4).path, list)
		self.assertIsInstance(n3.get_relation_to(n1).path, list)
		self.assertIsInstance(n3.get_relation_to(n2).path, list)
		self.assertIsInstance(n3.get_relation_to(n4).path, list)
		self.assertIsInstance(n4.get_relation_to(n1).path, list)
		self.assertIsInstance(n4.get_relation_to(n2).path, list)
		self.assertIsInstance(n4.get_relation_to(n3).path, list)

	def test_error_ungraphed_node(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		db.session.add(n5)
		db.session.commit()
		self.assertIsNone(n5.get_relation_to(n1).path)
		self.assertIsNone(n5.get_relation_to(n2).path)
		self.assertIsNone(n5.get_relation_to(n3).path)
		self.assertIsNone(n5.get_relation_to(n4).path)
		self.assertIsNone(n1.get_relation_to(n5).path)
		self.assertIsNone(n2.get_relation_to(n5).path)
		self.assertIsNone(n3.get_relation_to(n5).path)
		self.assertIsNone(n4.get_relation_to(n5).path)

	def test_non_adjacent_node_relations_with_one(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		Seed.link_new_member(n3,n5,type='wife')
		self.assertIsNotNone(n5.get_relation_to(n1).path)
		self.assertIsNotNone(n5.get_relation_to(n2).path)
		self.assertIsNotNone(n5.get_relation_to(n3).path)
		self.assertIsNotNone(n5.get_relation_to(n4).path)
		self.assertIsNotNone(n1.get_relation_to(n5).path)
		self.assertIsNotNone(n2.get_relation_to(n5).path)
		self.assertIsNotNone(n3.get_relation_to(n5).path)
		self.assertIsNotNone(n4.get_relation_to(n5).path)

	def test_non_adjacent_node_relations_with_two(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		n6 = Node(baptism_name='Andrew',dob=date(1960,7,5))
		Seed.link_new_member(n3,n5,type='wife')
		Seed.link_new_member(n3,n5,n6,type='child')
		self.assertIsNotNone(n6.get_relation_to(n1).path)
		self.assertIsNotNone(n6.get_relation_to(n2).path)
		self.assertIsNotNone(n6.get_relation_to(n3).path)
		self.assertIsNotNone(n6.get_relation_to(n4).path)
		self.assertIsNotNone(n6.get_relation_to(n5).path)
		self.assertIsNotNone(n1.get_relation_to(n6).path)
		self.assertIsNotNone(n2.get_relation_to(n6).path)
		self.assertIsNotNone(n3.get_relation_to(n6).path)
		self.assertIsNotNone(n4.get_relation_to(n6).path)
		self.assertIsNotNone(n5.get_relation_to(n6).path)

	def test_valid_undirgraph_edge_count(self):
		n1 = Node.query.get(1)
		data = n1.graph_output.edges(data=True)
		c1 = Seed.count_edge_labels(data=data)
		self.assertTrue(c1[1]==1)
		self.assertTrue(c1[2]==1)
		self.assertTrue(c1[3]==2)
		self.assertTrue(c1[4]==2)

	def test_valid_undirgraph_edge_count_with_one(self):
		n1 = Node.query.get(1)
		n3 = Node.query.get(3)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		Seed.link_new_member(n3,n5,type='wife')
		data = n1.graph_output.edges(data=True)
		c2 = Seed.count_edge_labels(data=data)
		self.assertTrue(c2[1]==2)
		self.assertTrue(c2[2]==1)
		self.assertTrue(c2[3]==2)
		self.assertTrue(c2[4]==2)

	def test_valid_undirgraph_edge_count_with_two(self):
		n1 = Node.query.get(1)
		n3 = Node.query.get(3)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		n6 = Node(baptism_name='Andrew',dob=date(1960,7,5))
		Seed.link_new_member(n3,n5,type='wife')
		Seed.link_new_member(n3,n5,n6,type='child')
		data = n1.graph_output.edges(data=True)
		c2 = Seed.count_edge_labels(data=data)
		self.assertTrue(c2[1]==2)
		self.assertTrue(c2[2]==1)
		self.assertTrue(c2[3]==2)
		self.assertTrue(c2[4]==4)