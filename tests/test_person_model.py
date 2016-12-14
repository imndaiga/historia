import unittest
from app import create_app, db
from app.models import Person, Link
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

    def test_person_count(self):
        self.assertTrue(Person.query.count() == 4)

    def test_link_count(self):
        self.assertTrue(Link.query.count() == 12)

    def test_valid_links(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        p3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        p4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        self.assertTrue(p1.link_ascends(p3))
        self.assertTrue(p1.link_ascends(p2))
        self.assertTrue(p1.link_ascends(p4))
        self.assertTrue(p2.link_ascends(p3))
        self.assertTrue(p2.link_ascends(p4))
        self.assertTrue(p3.link_ascends(p4))
        self.assertTrue(p1.link_descends(p3))
        self.assertTrue(p1.link_descends(p4))
        self.assertTrue(p2.link_descends(p3))
        self.assertTrue(p2.link_descends(p4))

    def test_valid_link_addition(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        p3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        p4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        a1 = Person(baptism_name='Coraline')
        self.seed.relate(parents=[p1, p2], children=[p3, p4, a1])
        self.assertTrue(Link.query.count() == 20)

    def test_valid_label_change(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        p3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        p4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        a1 = Person(baptism_name='Coraline')
        self.seed.relate(parents=[p1, p2], children=[p3, p4, a1])
        self.assertTrue(a1._change_link_label(p1, 1))
        self.assertTrue(a1._change_link_label(p2, 1))
        self.assertTrue(a1._change_link_label(p3, 0))
        self.assertTrue(a1._change_link_label(p4, 0))
        self.assertTrue(p1._change_link_label(a1, 1))
        self.assertTrue(p2._change_link_label(a1, 1))
        self.assertTrue(p3._change_link_label(a1, 0))
        self.assertTrue(p4._change_link_label(a1, 0))

    def test_invalid_label_change(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        p3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        p4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        a1 = Person(baptism_name='Coraline')
        db.session.add(a1)
        db.session.commit()
        self.assertFalse(a1._change_link_label(p1, 1))
        self.assertFalse(a1._change_link_label(p2, 1))
        self.assertFalse(a1._change_link_label(p3, 0))
        self.assertFalse(a1._change_link_label(p4, 0))
        self.assertFalse(p1._change_link_label(a1, 1))
        self.assertFalse(p2._change_link_label(a1, 1))
        self.assertFalse(p3._change_link_label(a1, 0))
        self.assertFalse(p4._change_link_label(a1, 0))

    def test_invalid_person_loop(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        self.assertFalse(p1._change_link_label(p1, 1))

    def test_valid_person_from_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        token = p1.generate_login_token(email=p1.email)
        sig_data = Person.person_from_token(token)
        self.assertTrue(sig_data['person'].email == p1.email)

    def test_invalid_person_from_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        token = p1.generate_login_token(email=p1.email)
        sig_data = Person.person_from_token(token)
        self.assertFalse(sig_data['person'].email == p2.email)

    def test_expired_person_from_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        token = p1.generate_login_token(email=p1.email, expiration=1)
        time.sleep(2)
        sig_data = Person.person_from_token(token)
        self.assertFalse(sig_data['sig'])

    def test_valid_login_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        token = p1.generate_login_token(email=p1.email)
        self.assertTrue(p1.confirm_login(token))

    def test_invalid_login_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        p2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        token = p1.generate_login_token(email=p1.email)
        self.assertFalse(p2.confirm_login(token))

    def test_expired_login_token(self):
        p1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        token = p1.generate_login_token(expiration=1, email=p1.email)
        time.sleep(2)
        self.assertFalse(p1.confirm_login(token))
