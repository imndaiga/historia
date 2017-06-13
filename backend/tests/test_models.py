import unittest
from app import create_app, db, seed
from app.models import Person


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed.run(family_units=1, family_size=4, layers=0, verbose=False)
        self.p1 = db.session.query(Person).filter_by(
            first_name='Tina').first()
        self.p2 = db.session.query(Person).filter_by(
            first_name='Patricia').first()
        self.p3 = db.session.query(Person).filter_by(
            first_name='Paige').first()
        self.p4 = db.session.query(Person).filter_by(
            first_name='Kerry').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_person_count(self):
        self.assertTrue(Person.query.count() == 4)
