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
        graph.clear()
        seed.run(units=1, size=4, layers=0, verbose=False)
        self.p1 = db.session.query(Person).filter_by(
            first_name='Scott').first()
        self.p2 = db.session.query(Person).filter_by(
            first_name='Nicola').first()
        self.p3 = db.session.query(Person).filter_by(
            first_name='Rosemary').first()
        self.p4 = db.session.query(Person).filter_by(
            first_name='Francesca').first()

    @staticmethod
    def reset():
        db.session.remove()
        db.drop_all()
        db.create_all()
        graph.clear()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seed_count_is_valid(self):
        relative = fake.family_member(sex='Female')
        a1 = Person(
            first_name=relative['first_name'],
            last_name=relative['last_name'],
            ethnic_name=relative['ethnic_name'],
            sex=relative['sex'],
            birth_date=relative['birth_date'],
            email=relative['email'],
            confirmed=False
        )
        db.session.add(a1)
        db.session.commit()
        self.p1.get_or_create_relation(self.p2, 1)
        self.p1.get_or_create_relation(self.p3, 3)
        self.p1.get_or_create_relation(self.p4, 3)
        self.p1.get_or_create_relation(a1, 3)
        self.p2.get_or_create_relation(self.p3, 3)
        self.p2.get_or_create_relation(self.p4, 3)
        self.p2.get_or_create_relation(a1, 3)
        self.p3.get_or_create_relation(self.p4, 2)
        self.p3.get_or_create_relation(a1, 2)
        self.p4.get_or_create_relation(a1, 2)
        self.assertEqual(Link.query.count(), 20)

    def test_seed_link_count_is_valid(self):
        self.assertEqual(Link.query.count(), 12)

    def test_seed_person_link_count_with_one_layer_and_family_size_3(self):
        self.reset()
        seed.run(units=1, size=3, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 9)
        self.assertEqual(Link.query.count(), 24)

    def test_seed_person_link_count_with_one_layer_and_family_size_4(self):
        self.reset()
        seed.run(units=1, size=4, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 16)
        self.assertEqual(Link.query.count(), 60)

    def test_seed_person_link_count_with_one_layer_and_family_size_5(self):
        self.reset()
        seed.run(units=1, size=5, layers=1, verbose=False)
        self.assertEqual(Person.query.count(), 25)
        self.assertEqual(Link.query.count(), 120)
