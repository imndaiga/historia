import unittest
from app import create_app, db
from app.models import Node, GlobalEdge
from app.seed import Seed
import time


class NodeModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.seed = Seed(app=self.app)
        self.seed.run()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
        self.seed.relate(parents=[n1, n2], children=[n3, n4, a1])
        self.assertTrue(GlobalEdge.query.count() == 20)

    def test_valid_label_change(self):
        n1 = db.session.query(Node).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Node).filter_by(baptism_name='Christine').first()
        n3 = db.session.query(Node).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Node).filter_by(baptism_name='Carol').first()
        a1 = Node(baptism_name='Coraline')
        self.seed.relate(parents=[n1, n2], children=[n3, n4, a1])
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
