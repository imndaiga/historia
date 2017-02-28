import unittest
from app import db, create_app, seed, graph
from app.seed import fake
from app.models import Link, Person


class SeedTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed.auto = False
        graph.clear()
        seed.run(family_units=1, family_size=4)
        self.p1 = db.session.query(Person).filter_by(
            baptism_name='Mandy').first()
        self.p2 = db.session.query(Person).filter_by(
            baptism_name='Laura').first()
        self.p3 = db.session.query(Person).filter_by(
            baptism_name='Dawn').first()
        self.p4 = db.session.query(Person).filter_by(
            baptism_name='Ashley').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seed_count_is_valid(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(parents=[self.p1, self.p2],
                    children=[self.p3, self.p4, a1])
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
        seed.run(family_units=1, family_size=4)
        G = graph.current
        self.assertTrue(G.order() == 4)
        self.assertTrue(G.size() == 12)
