import unittest
from app import create_app, db
from app.models import Node, GlobalEdge
from datetime import date
import time
import networkx as nx

class NodeModelTestCase(unittest.TestCase):
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
		self.link_new_member(n1,n2,n3,n4,n5,type='daughter')
		self.assertTrue(GlobalEdge.query.count() == 20)

	def test_valid_label_change(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		self.link_new_member(n1,n2,n3,n4,n5,type='daughter')
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
		self.assertTrue(isinstance(n1.graph_output.nodes(), list))
		self.assertTrue(isinstance(n1.graph_output.edges(), list))

	def test_count_node_undirgraph_elements(self):
		n1 = Node.query.get(1)
		self.assertTrue(n1.graph_output.number_of_edges()==6)
		self.assertTrue(n1.graph_output.number_of_nodes()==4)

	def test_pre_existing_node_relations(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		self.assertTrue(n1.node_relation(n2))
		self.assertTrue(n1.node_relation(n3))
		self.assertTrue(n1.node_relation(n4))
		self.assertTrue(n2.node_relation(n1))
		self.assertTrue(n2.node_relation(n3))
		self.assertTrue(n2.node_relation(n4))
		self.assertTrue(n3.node_relation(n1))
		self.assertTrue(n3.node_relation(n2))
		self.assertTrue(n3.node_relation(n4))
		self.assertTrue(n4.node_relation(n1))
		self.assertTrue(n4.node_relation(n2))
		self.assertTrue(n4.node_relation(n3))

	def test_error_ungraphed_node(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		db.session.add(n5)
		db.session.commit()
		with self.assertRaises(KeyError):
			n5.node_relation(n1)
			n5.node_relation(n2)
			n5.node_relation(n3)
			n5.node_relation(n4)
			n1.node_relation(n5)
			n2.node_relation(n5)
			n3.node_relation(n5)
			n4.node_relation(n5)

	def test_positive_non_adjacent_node_relations(self):
		(n1,n2,n3,n4) = Node.query.slice(0,4)
		n5 = Node(baptism_name='Coraline',dob=date(1940,7,5))
		self.link_new_member(n3,n5,type='wife')
		self.assertTrue(n5.node_relation(n1))
		self.assertTrue(n5.node_relation(n2))
		self.assertTrue(n5.node_relation(n3))
		self.assertTrue(n5.node_relation(n4))
		self.assertTrue(n1.node_relation(n5))
		self.assertTrue(n2.node_relation(n5))
		self.assertTrue(n3.node_relation(n5))
		self.assertTrue(n4.node_relation(n5))

	@staticmethod
	def link_new_member(*args, **kwargs):
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