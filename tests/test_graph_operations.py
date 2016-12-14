import unittest
from app import create_app, db, graph, seed
from app.models import Person


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        graph.clear()
        seed.run()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        graph.clear()

    def test_subgraph_count(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n1_subgraph = graph.get_subgraph(source=n1)
        self.assertTrue(n1_subgraph.number_of_edges() == 3)
        self.assertTrue(n1_subgraph.number_of_nodes() == 4)

    def test_subgraph_basic_relations(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        n1_n2_relation = graph._relations_list(source=n1, target=n2)
        n1_n3_relation = graph._relations_list(source=n1, target=n3)
        n1_n4_relation = graph._relations_list(source=n1, target=n4)
        n2_n1_relation = graph._relations_list(source=n2, target=n1)
        n2_n3_relation = graph._relations_list(source=n2, target=n3)
        n2_n4_relation = graph._relations_list(source=n2, target=n4)
        n3_n1_relation = graph._relations_list(source=n3, target=n1)
        n3_n2_relation = graph._relations_list(source=n3, target=n2)
        n3_n4_relation = graph._relations_list(source=n3, target=n4)
        n4_n1_relation = graph._relations_list(source=n4, target=n1)
        n4_n2_relation = graph._relations_list(source=n4, target=n2)
        n4_n3_relation = graph._relations_list(source=n4, target=n3)
        self.assertTrue(n1_n2_relation == ['partner'])
        self.assertTrue(n1_n3_relation == ['parent'])
        self.assertTrue(n1_n4_relation == ['parent'])
        self.assertTrue(n2_n1_relation == ['partner'])
        self.assertTrue(n2_n3_relation == ['parent'])
        self.assertTrue(n2_n4_relation == ['parent'])
        self.assertTrue(n3_n1_relation == ['child'])
        self.assertTrue(n3_n2_relation == ['child'])
        self.assertTrue(n3_n4_relation == ['sibling'])
        self.assertTrue(n4_n1_relation == ['child'])
        self.assertTrue(n4_n2_relation == ['child'])
        self.assertTrue(n4_n3_relation == ['sibling'])

    def test_subgraph_null_relations(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n2 = db.session.query(Person).filter_by(
            baptism_name='Christine').first()
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        n4 = db.session.query(Person).filter_by(baptism_name='Carol').first()
        a1 = Person(baptism_name='Coraline')
        db.session.add(a1)
        db.session.commit()
        with self.assertRaises(KeyError):
            graph._relations_list(source=a1, target=n1)
            graph._relations_list(source=a1, target=n2)
            graph._relations_list(source=a1, target=n3)
            graph._relations_list(source=a1, target=n4)
            graph._relations_list(source=n1, target=a1)
            graph._relations_list(source=n2, target=a1)
            graph._relations_list(source=n3, target=a1)
            graph._relations_list(source=n4, target=a1)

    def test_subgraph_edge_count_parent(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n1_subgraph = graph.get_subgraph(source=n1)
        data = n1_subgraph.edges(data=True)
        c1 = seed.count_subgraph_weights(data=data)
        self.assertTrue(c1.get(1) == 1)
        self.assertIsNone(c1.get(2))
        self.assertTrue(c1.get(3) == 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child(self):
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        n3_subgraph = graph.get_subgraph(source=n3)
        data = n3_subgraph.edges(data=True)
        c2 = seed.count_subgraph_weights(data=data)
        self.assertIsNone(c2.get(1))
        self.assertTrue(c2.get(2) == 1)
        self.assertIsNone(c2.get(3))
        self.assertTrue(c2.get(4) == 2)

    def test_subgraph_edge_count_parent_in_law(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        a1 = Person(baptism_name='Coraline')
        seed.relate(partners=[n3, a1])
        graph.update()
        n1_subgraph = graph.get_subgraph(source=n1)
        data = n1_subgraph.edges(data=True)
        c3 = seed.count_subgraph_weights(data=data)
        self.assertTrue(c3.get(1) == 2)
        self.assertIsNone(c3.get(2))
        self.assertTrue(c3.get(3) == 2)
        self.assertIsNone(c3.get(4))

    def test_subgraph_edge_count_child_in_law(self):
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        a1 = Person(baptism_name='Coraline')
        seed.relate(partners=[n3, a1])
        graph.update()
        a1_subgraph = graph.get_subgraph(source=a1)
        data = a1_subgraph.edges(data=True)
        c4 = seed.count_subgraph_weights(data=data)
        self.assertTrue(c4.get(1) == 1)
        self.assertTrue(c4.get(2) == 1)
        self.assertIsNone(c4.get(3))
        self.assertTrue(c4.get(4) == 2)

    def test_subgraph_edge_count_grandchild(self):
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        a1 = Person(baptism_name='Coraline')
        a2 = Person(baptism_name='Andrew')
        seed.relate(parents=[n3, a1], children=[a2])
        graph.update()
        a2_subgraph = graph.get_subgraph(source=a2)
        data = a2_subgraph.edges(data=True)
        c5 = seed.count_subgraph_weights(data=data)
        self.assertIsNone(c5.get(1))
        self.assertTrue(c5.get(2) == 1)
        self.assertIsNone(c5.get(3))
        self.assertTrue(c5.get(4) == 4)

    def test_subgraph_edge_count_grandparent(self):
        n1 = db.session.query(Person).filter_by(baptism_name='Chris').first()
        n3 = db.session.query(Person).filter_by(baptism_name='Charlie').first()
        a1 = Person(baptism_name='Coraline')
        a2 = Person(baptism_name='Andrew')
        seed.relate(parents=[n3, a1], children=[a2])
        graph.update()
        n1_subgraph = graph.get_subgraph(source=n1)
        data = n1_subgraph.edges(data=True)
        c6 = seed.count_subgraph_weights(data=data)
        self.assertTrue(c6.get(1) == 2)
        self.assertIsNone(c6.get(2))
        self.assertTrue(c6.get(3) == 3)
        self.assertIsNone(c6.get(4))
