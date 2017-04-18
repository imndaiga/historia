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
        seed.run(family_units=1, family_size=4, layers=0, verbose=False)
        self.p1 = db.session.query(Person).filter_by(
            baptism_name='Tina').first()
        self.p2 = db.session.query(Person).filter_by(
            baptism_name='Patricia').first()
        self.p3 = db.session.query(Person).filter_by(
            baptism_name='Paige').first()
        self.p4 = db.session.query(Person).filter_by(
            baptism_name='Kerry').first()

    @staticmethod
    def reset():
        db.session.remove()
        db.drop_all()
        db.create_all()
        graph.clear()
        seed.auto = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seed_count_is_valid(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            last_name=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(parents=[self.p1, self.p2],
                    children=[self.p3, self.p4, a1])
        self.assertEqual(Link.query.count(), 20)

    def test_seed_link_count_is_valid(self):
        self.assertEqual(Link.query.count(), 12)

    def test_seed_auto_graph_is_false(self):
        G = graph.current
        self.assertEqual(G.order(), 0)
        self.assertEqual(G.size(), 0)

    def test_seed_auto_graph_is_true(self):
        seed.auto = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        seed.auto = True
        seed.run(family_units=1, family_size=4, layers=0, verbose=False)
        G = graph.current
        self.assertEqual(G.order(), 4)
        self.assertEqual(G.size(), 12)

    def test_seed_person_link_count_with_one_layer_and_family_size_3(self):
        self.reset()
        seed.run(family_units=1, family_size=3, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 9)
        self.assertEqual(Link.query.count(), 24)

    def test_seed_person_link_count_with_one_layer_and_family_size_4(self):
        self.reset()
        seed.run(family_units=1, family_size=4, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 16)
        self.assertEqual(Link.query.count(), 60)

    def test_seed_person_link_count_with_one_layer_and_family_size_5(self):
        self.reset()
        seed.run(family_units=1, family_size=5, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 25)
        self.assertEqual(Link.query.count(), 120)
