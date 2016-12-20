import unittest
from app import db, create_app, seed, graph
from app.models import Link, Person


class SeedTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed.auto = False
        graph.clear()
        seed.run()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seed_count_is_valid(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        p3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        p4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        a1 = Person(baptism_name='Coraline')
        seed.relate(parents=[p1, p2], children=[p3, p4, a1])
        self.assertTrue(Link.query.count() == 20)

    def test_seed_link_count_is_valid(self):
        self.assertTrue(Link.query.count() == 12)

    def test_seed_auto_graph_is_false(self):
        G = graph.current
        self.assertTrue(G.order() == 0)
        self.assertTrue(G.size() == 0)

    def test_seed_auto_graph_is_true(self):
        seed.auto = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        seed.auto = True
        seed.run()
        G = graph.current
        self.assertTrue(G.order() == 4)
        self.assertTrue(G.size() == 12)
