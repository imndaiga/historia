import unittest
from app import create_app, db, seed
from app.models import Person
from app.seed import fake


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        seed.run(family_units=1, family_size=4, layers=0, verbose=False)
        self.p1 = db.session.query(Person).filter_by(
            baptism_name='Tina').first()
        self.p2 = db.session.query(Person).filter_by(
            baptism_name='Patricia').first()
        self.p3 = db.session.query(Person).filter_by(
            baptism_name='Paige').first()
        self.p4 = db.session.query(Person).filter_by(
            baptism_name='Kerry').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_person_count(self):
        self.assertTrue(Person.query.count() == 4)

    def test_links(self):
        self.assertTrue(self.p1.link_ascends(self.p3))
        self.assertTrue(self.p1.link_ascends(self.p2))
        self.assertTrue(self.p1.link_ascends(self.p4))
        self.assertTrue(self.p2.link_ascends(self.p3))
        self.assertTrue(self.p2.link_ascends(self.p4))
        self.assertTrue(self.p3.link_ascends(self.p4))
        self.assertTrue(self.p1.link_descends(self.p3))
        self.assertTrue(self.p1.link_descends(self.p4))
        self.assertTrue(self.p2.link_descends(self.p3))
        self.assertTrue(self.p2.link_descends(self.p4))

    def test_valid_link_label_changes(self):
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
        self.assertTrue(a1._change_link_label(self.p1, 1))
        self.assertTrue(a1._change_link_label(self.p2, 1))
        self.assertTrue(a1._change_link_label(self.p3, 0))
        self.assertTrue(a1._change_link_label(self.p4, 0))
        self.assertTrue(self.p1._change_link_label(a1, 1))
        self.assertTrue(self.p2._change_link_label(a1, 1))
        self.assertTrue(self.p3._change_link_label(a1, 0))
        self.assertTrue(self.p4._change_link_label(a1, 0))

    def test_invalid_link_label_changes(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            last_name=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        db.session.add(a1)
        db.session.commit()
        self.assertFalse(a1._change_link_label(self.p1, 1))
        self.assertFalse(a1._change_link_label(self.p2, 1))
        self.assertFalse(a1._change_link_label(self.p3, 0))
        self.assertFalse(a1._change_link_label(self.p4, 0))
        self.assertFalse(self.p1._change_link_label(a1, 1))
        self.assertFalse(self.p2._change_link_label(a1, 1))
        self.assertFalse(self.p3._change_link_label(a1, 0))
        self.assertFalse(self.p4._change_link_label(a1, 0))

    def test_invalid_person_self_loop(self):
        self.assertFalse(self.p1._change_link_label(self.p1, 1))
