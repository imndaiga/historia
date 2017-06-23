import unittest
from app import create_app, db, forge
from app.models import Person


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        forge.run(units=1, size=4, layers=0, verbose=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_person_count(self):
        self.assertTrue(Person.query.count() == 4)
