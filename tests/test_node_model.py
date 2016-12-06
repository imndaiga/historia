import unittest
from app import create_app, db
from app.models import Node, GlobalEdge, Seed
from datetime import date
import time
import os


class NodeModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        if 'graph-test.gpickle' in self.app.config['GRAPH_PATH'] \
                and os.path.exists(self.app.config['GRAPH_PATH']):
            os.remove(self.app.config['GRAPH_PATH'])
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
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
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
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        Seed.link_new_member(n1, n2, n3, n4, n5, type='daughter')
        self.assertTrue(GlobalEdge.query.count() == 20)

    def test_valid_label_change(self):
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        Seed.link_new_member(n1, n2, n3, n4, n5, type='daughter')
        self.assertTrue(n5._change_edge_label(n1, 1))
        self.assertTrue(n5._change_edge_label(n2, 1))
        self.assertTrue(n5._change_edge_label(n3, 0))
        self.assertTrue(n5._change_edge_label(n4, 0))
        self.assertTrue(n1._change_edge_label(n5, 1))
        self.assertTrue(n2._change_edge_label(n5, 1))
        self.assertTrue(n3._change_edge_label(n5, 0))
        self.assertTrue(n4._change_edge_label(n5, 0))

    def test_invalid_label_change(self):
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        db.session.add(n5)
        db.session.commit()
        self.assertFalse(n5._change_edge_label(n1, 1))
        self.assertFalse(n5._change_edge_label(n2, 1))
        self.assertFalse(n5._change_edge_label(n3, 0))
        self.assertFalse(n5._change_edge_label(n4, 0))
        self.assertFalse(n1._change_edge_label(n5, 1))
        self.assertFalse(n2._change_edge_label(n5, 1))
        self.assertFalse(n3._change_edge_label(n5, 0))
        self.assertFalse(n4._change_edge_label(n5, 0))

    def test_invalid_node_loop(self):
        n1 = Node.query.get(1)
        self.assertFalse(n1.create_edge(n1, 1))
        self.assertFalse(n1._change_edge_label(n1, 1))

    def test_valid_node_from_token(self):
        n1 = Node.query.get(1)
        token = n1.generate_login_token(email=n1.email)
        sig_data = Node.node_from_token(token)
        self.assertTrue(sig_data['node'].email == n1.email)

    def test_invalid_node_from_token(self):
        (n1, n2) = Node.query.slice(0, 2)
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
        (n1, n2) = Node.query.slice(0, 2)
        token = n1.generate_login_token(email=n1.email)
        self.assertFalse(n2.confirm_login(token))

    def test_expired_login_token(self):
        n1 = Node.query.get(1)
        token = n1.generate_login_token(expiration=1, email=n1.email)
        time.sleep(2)
        self.assertFalse(n1.confirm_login(token))

    def test_subgraph_count(self):
        n1 = Node.query.get(1)
        self.assertTrue(n1.subgraph.number_of_edges() == 3)
        self.assertTrue(n1.subgraph.number_of_nodes() == 4)

    def test_subgraph_basic_relations(self):
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
        self.assertTrue(n1._resolve_relation(target=n2) == ['partner'])
        self.assertTrue(n1._resolve_relation(target=n3) == ['parent'])
        self.assertTrue(n1._resolve_relation(target=n4) == ['parent'])
        self.assertTrue(n2._resolve_relation(target=n1) == ['partner'])
        self.assertTrue(n2._resolve_relation(target=n3) == ['parent'])
        self.assertTrue(n2._resolve_relation(target=n4) == ['parent'])
        self.assertTrue(n3._resolve_relation(target=n1) == ['child'])
        self.assertTrue(n3._resolve_relation(target=n2) == ['child'])
        self.assertTrue(n3._resolve_relation(target=n4) == ['sibling'])
        self.assertTrue(n4._resolve_relation(target=n1) == ['child'])
        self.assertTrue(n4._resolve_relation(target=n2) == ['child'])
        self.assertTrue(n4._resolve_relation(target=n3) == ['sibling'])

    def test_subgraph_null_relations(self):
        (n1, n2, n3, n4) = Node.query.slice(0, 4)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        db.session.add(n5)
        db.session.commit()
        with self.assertRaises(KeyError):
            n5._resolve_relation(target=n1)
            n5._resolve_relation(target=n2)
            n5._resolve_relation(target=n3)
            n5._resolve_relation(target=n4)
            n1._resolve_relation(target=n5)
            n2._resolve_relation(target=n5)
            n3._resolve_relation(target=n5)
            n4._resolve_relation(target=n5)

    def test_subgraph_edge_count_parent(self):
        n1 = Node.query.get(1)
        data = n1.subgraph.edges(data=True)
        c1 = Seed.count_edge_labels(data=data)
        self.assertTrue(c1.get(1) == 1)
        self.assertIsNone(c1.get(2))
        self.assertTrue(c1.get(3) == 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child(self):
        n3 = Node.query.get(3)
        data = n3.subgraph.edges(data=True)
        c2 = Seed.count_edge_labels(data=data)
        self.assertIsNone(c2.get(1))
        self.assertTrue(c2.get(2) == 1)
        self.assertIsNone(c2.get(3))
        self.assertTrue(c2.get(4) == 2)

    def test_subgraph_edge_count_parent_in_law(self):
        n1 = Node.query.get(1)
        n3 = Node.query.get(3)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        Seed.link_new_member(n3, n5, type='wife')
        data = n1.subgraph.edges(data=True)
        c3 = Seed.count_edge_labels(data=data)
        self.assertTrue(c3.get(1) == 2)
        self.assertIsNone(c3.get(2))
        self.assertTrue(c3.get(3) == 2)
        self.assertIsNone(c3.get(4))

    def test_subgraph_edge_count_child_in_law(self):
        n3 = Node.query.get(3)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        Seed.link_new_member(n3, n5, type='wife')
        data = n5.subgraph.edges(data=True)
        c4 = Seed.count_edge_labels(data=data)
        self.assertTrue(c4.get(1) == 1)
        self.assertTrue(c4.get(2) == 1)
        self.assertIsNone(c4.get(3))
        self.assertTrue(c4.get(4) == 2)

    def test_subgraph_edge_count_grandchild(self):
        n3 = Node.query.get(3)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        n6 = Node(baptism_name='Andrew', dob=date(1960, 7, 5))
        Seed.link_new_member(n3, n5, type='wife')
        Seed.link_new_member(n3, n5, n6, type='child')
        data = n6.subgraph.edges(data=True)
        c5 = Seed.count_edge_labels(data=data)
        self.assertIsNone(c5.get(1))
        self.assertTrue(c5.get(2) == 1)
        self.assertIsNone(c5.get(3))
        self.assertTrue(c5.get(4) == 4)

    def test_subgraph_edge_count_grandparent(self):
        n1 = Node.query.get(1)
        n3 = Node.query.get(3)
        n5 = Node(baptism_name='Coraline', dob=date(1940, 7, 5))
        n6 = Node(baptism_name='Andrew', dob=date(1960, 7, 5))
        Seed.link_new_member(n3, n5, type='wife')
        Seed.link_new_member(n3, n5, n6, type='child')
        data = n1.subgraph.edges(data=True)
        c6 = Seed.count_edge_labels(data=data)
        self.assertTrue(c6.get(1) == 2)
        self.assertIsNone(c6.get(2))
        self.assertTrue(c6.get(3) == 3)
        self.assertIsNone(c6.get(4))
