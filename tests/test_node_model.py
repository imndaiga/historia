import unittest
from app import create_app, db
from app.models import Node, GlobalEdge, GlobalGraph, Seed
import time


class NodeModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.graph = GlobalGraph(self.app)
        self.graph.clear()
        Seed.run()
        self.graph.update()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.graph.clear()

    def test_node_count(self):
        self.assertTrue(Node.query.count() == 4)

    def test_edge_count(self):
        self.assertTrue(GlobalEdge.query.count() == 12)

    def test_valid_edges(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
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
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
        a1 = Node(baptism_name='Coraline')
        Seed.relate(parents=[n1, n2], children=[n3, n4, a1])
        self.graph.update()
        self.assertTrue(GlobalEdge.query.count() == 20)

    def test_valid_label_change(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
        a1 = Node(baptism_name='Coraline')
        Seed.relate(parents=[n1, n2], children=[n3, n4, a1])
        self.assertTrue(a1._change_edge_label(n1, 1))
        self.assertTrue(a1._change_edge_label(n2, 1))
        self.assertTrue(a1._change_edge_label(n3, 0))
        self.assertTrue(a1._change_edge_label(n4, 0))
        self.assertTrue(n1._change_edge_label(a1, 1))
        self.assertTrue(n2._change_edge_label(a1, 1))
        self.assertTrue(n3._change_edge_label(a1, 0))
        self.assertTrue(n4._change_edge_label(a1, 0))

    def test_invalid_label_change(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
        a1 = Node(baptism_name='Coraline')
        db.session.add(a1)
        db.session.commit()
        self.assertFalse(a1._change_edge_label(n1, 1))
        self.assertFalse(a1._change_edge_label(n2, 1))
        self.assertFalse(a1._change_edge_label(n3, 0))
        self.assertFalse(a1._change_edge_label(n4, 0))
        self.assertFalse(n1._change_edge_label(a1, 1))
        self.assertFalse(n2._change_edge_label(a1, 1))
        self.assertFalse(n3._change_edge_label(a1, 0))
        self.assertFalse(n4._change_edge_label(a1, 0))

    def test_invalid_node_loop(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        self.assertFalse(n1._change_edge_label(n1, 1))

    def test_valid_node_from_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        token = n1.generate_login_token(email=n1.email)
        sig_data = Node.node_from_token(token)
        self.assertTrue(sig_data['node'].email == n1.email)

    def test_invalid_node_from_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        token = n1.generate_login_token(email=n1.email)
        sig_data = Node.node_from_token(token)
        self.assertFalse(sig_data['node'].email == n2.email)

    def test_expired_node_from_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        token = n1.generate_login_token(email=n1.email, expiration=1)
        time.sleep(2)
        sig_data = Node.node_from_token(token)
        self.assertFalse(sig_data['sig'])

    def test_valid_login_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        token = n1.generate_login_token(email=n1.email)
        self.assertTrue(n1.confirm_login(token))

    def test_invalid_login_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        token = n1.generate_login_token(email=n1.email)
        self.assertFalse(n2.confirm_login(token))

    def test_expired_login_token(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        token = n1.generate_login_token(expiration=1, email=n1.email)
        time.sleep(2)
        self.assertFalse(n1.confirm_login(token))

    def test_subgraph_count(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        self.assertTrue(n1.subgraph.number_of_edges() == 3)
        self.assertTrue(n1.subgraph.number_of_nodes() == 4)

    def test_subgraph_basic_relations(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
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
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
        a1 = Node(baptism_name='Coraline')
        db.session.add(a1)
        db.session.commit()
        with self.assertRaises(KeyError):
            a1._resolve_relation(target=n1)
            a1._resolve_relation(target=n2)
            a1._resolve_relation(target=n3)
            a1._resolve_relation(target=n4)
            n1._resolve_relation(target=a1)
            n2._resolve_relation(target=a1)
            n3._resolve_relation(target=a1)
            n4._resolve_relation(target=a1)

    def test_subgraph_edge_count_parent(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        data = n1.subgraph.edges(data=True)
        c1 = Seed.count_edge_labels(data=data)
        self.assertTrue(c1.get(1) == 1)
        self.assertIsNone(c1.get(2))
        self.assertTrue(c1.get(3) == 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child(self):
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        data = n3.subgraph.edges(data=True)
        c2 = Seed.count_edge_labels(data=data)
        self.assertIsNone(c2.get(1))
        self.assertTrue(c2.get(2) == 1)
        self.assertIsNone(c2.get(3))
        self.assertTrue(c2.get(4) == 2)

    def test_subgraph_edge_count_parent_in_law(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        a1 = Node(baptism_name='Coraline')
        Seed.relate(partners=[n3, a1])
        self.graph.update()
        data = n1.subgraph.edges(data=True)
        c3 = Seed.count_edge_labels(data=data)
        self.assertTrue(c3.get(1) == 2)
        self.assertIsNone(c3.get(2))
        self.assertTrue(c3.get(3) == 2)
        self.assertIsNone(c3.get(4))

    def test_subgraph_edge_count_child_in_law(self):
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        a1 = Node(baptism_name='Coraline')
        Seed.relate(partners=[n3, a1])
        self.graph.update()
        data = a1.subgraph.edges(data=True)
        c4 = Seed.count_edge_labels(data=data)
        self.assertTrue(c4.get(1) == 1)
        self.assertTrue(c4.get(2) == 1)
        self.assertIsNone(c4.get(3))
        self.assertTrue(c4.get(4) == 2)

    def test_subgraph_edge_count_grandchild(self):
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        a1 = Node(baptism_name='Coraline')
        a2 = Node(baptism_name='Andrew')
        Seed.relate(parents=[n3, a1], children=[a2])
        self.graph.update()
        data = a2.subgraph.edges(data=True)
        c5 = Seed.count_edge_labels(data=data)
        self.assertIsNone(c5.get(1))
        self.assertTrue(c5.get(2) == 1)
        self.assertIsNone(c5.get(3))
        self.assertTrue(c5.get(4) == 4)

    def test_subgraph_edge_count_grandparent(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        a1 = Node(baptism_name='Coraline')
        a2 = Node(baptism_name='Andrew')
        Seed.relate(parents=[n3, a1], children=[a2])
        self.graph.update()
        data = n1.subgraph.edges(data=True)
        c6 = Seed.count_edge_labels(data=data)
        self.assertTrue(c6.get(1) == 2)
        self.assertIsNone(c6.get(2))
        self.assertTrue(c6.get(3) == 3)
        self.assertIsNone(c6.get(4))
