import unittest
from app import create_app, db, seed
from app.models import Person
from app.seed import fake
import time


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
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
            surname=relative['name'].split()[1],
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
            surname=relative['name'].split()[1],
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

    def test_valid_person_from_token(self):
        token = self.p1.generate_login_token(email=self.p1.email)
        sig_data = Person.person_from_token(token)
        self.assertTrue(sig_data['person'].email == self.p1.email)

    def test_invalid_person_from_token(self):
        token = self.p1.generate_login_token(email=self.p1.email)
        sig_data = Person.person_from_token(token)
        self.assertFalse(sig_data['person'].email == self.p2.email)

    def test_expired_person_from_token(self):
        token = self.p1.generate_login_token(email=self.p1.email, expiration=1)
        time.sleep(2)
        sig_data = Person.person_from_token(token)
        self.assertFalse(sig_data['sig'])

    def test_valid_login_token(self):
        token = self.p1.generate_login_token(email=self.p1.email)
        self.assertTrue(self.p1.confirm_login(token))

    def test_invalid_login_token(self):
        token = self.p1.generate_login_token(email=self.p1.email)
        self.assertFalse(self.p2.confirm_login(token))

    def test_expired_login_token(self):
        token = self.p1.generate_login_token(expiration=1, email=self.p1.email)
        time.sleep(2)
        self.assertFalse(self.p1.confirm_login(token))
