import unittest
from app import create_app, db, graph, forge
from app.faker import fake
from app.models import Person
import os


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.GG = graph.GlobalGraph

        db.create_all()
        self.GG.clear()

        person_families, _ = forge.run(
            units=1,
            size=4,
            layers=0,
            verbose=False
        )

        self.p1, self.p2 = person_families[0]['parents']
        self.p3, self.p4 = person_families[0]['children']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.GG.clear()
        self.app_context.pop()

    def reset(self):
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.GG.clear()

    def delete_gpickle_file(self):
        if os.path.exists(self.app.config['GRAPH_PATH']):
            os.remove(self.app.config['GRAPH_PATH'])

    def test_graph_is_testing(self):
        self.assertTrue('graph-test.gpickle' in self.app.config['GRAPH_PATH'])

    def test_graph_load_with_invalid_environment_variable(self):
        graph.gpickle_path = None
        with self.assertRaises(EnvironmentError):
            graph._get_or_create_global_graph()

    def test_graph_load_instatiates_gpickle_file(self):
        self.delete_gpickle_file()
        self.assertFalse(os.path.exists(self.app.config['GRAPH_PATH']))
        self.assertTrue(os.path.exists(self.app.config['GRAPH_PATH']))
        self.assertEqual(self.GG.order(), 0)
        self.assertEqual(self.GG.size(), 0)

    def test_graph_load_is_successful(self):
        self.assertEqual(self.GG.order(), 4)
        self.assertEqual(self.GG.size(), 12)

    def test_graph_update_is_successful(self):
        self.delete_gpickle_file()
        self.assertEqual(self.GG.order(), 0)
        self.assertEqual(self.GG.size(), 0)
        graph.update()
        self.assertEqual(self.GG.order(), 4)
        self.assertEqual(self.GG.size(), 12)

    def test_graph_clear_is_successful(self):
        self.GG.clear()
        self.assertEqual(self.GG.order(), 0)
        self.assertEqual(self.GG.size(), 0)

    def test_graph_has_no_selfloops(self):
        self.assertEqual(self.GG.number_of_selfloops(), 0)

    def test_graph_get_subgraph_is_successful(self):
        n1_subgraph = self.p1.get_graph()
        self.assertEqual(n1_subgraph.number_of_edges(), 3)
        self.assertEqual(n1_subgraph.number_of_nodes(), 4)

    def test_subgraph_basic_relations(self):
        n1_n2_relation = graph.get_relationship(
            source_person=self.p1, target_person=self.p2)
        n1_n3_relation = graph.get_relationship(
            source_person=self.p1, target_person=self.p3)
        n1_n4_relation = graph.get_relationship(
            source_person=self.p1, target_person=self.p4)
        n2_n1_relation = graph.get_relationship(
            source_person=self.p2, target_person=self.p1)
        n2_n3_relation = graph.get_relationship(
            source_person=self.p2, target_person=self.p3)
        n2_n4_relation = graph.get_relationship(
            source_person=self.p2, target_person=self.p4)
        n3_n1_relation = graph.get_relationship(
            source_person=self.p3, target_person=self.p1)
        n3_n2_relation = graph.get_relationship(
            source_person=self.p3, target_person=self.p2)
        n3_n4_relation = graph.get_relationship(
            source_person=self.p3, target_person=self.p4)
        n4_n1_relation = graph.get_relationship(
            source_person=self.p4, target_person=self.p1)
        n4_n2_relation = graph.get_relationship(
            source_person=self.p4, target_person=self.p2)
        n4_n3_relation = graph.get_relationship(
            source_person=self.p4, target_person=self.p3)

        self.assertEqual(n1_n2_relation, 'Partner')
        self.assertEqual(n1_n3_relation, 'Parent')
        self.assertEqual(n1_n4_relation, 'Parent')
        self.assertEqual(n2_n1_relation, 'Partner')
        self.assertEqual(n2_n3_relation, 'Parent')
        self.assertEqual(n2_n4_relation, 'Parent')
        self.assertEqual(n3_n1_relation, 'Child')
        self.assertEqual(n3_n2_relation, 'Child')
        self.assertEqual(n3_n4_relation, 'Sibling')
        self.assertEqual(n4_n1_relation, 'Child')
        self.assertEqual(n4_n2_relation, 'Child')
        self.assertEqual(n4_n3_relation, 'Sibling')

    def test_subgraph_null_relations(self):
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
        with self.assertRaises(KeyError):
            graph.get_relationship(source_person=a1, target_person=self.p1)
            graph.get_relationship(source_person=a1, target_person=self.p2)
            graph.get_relationship(source_person=a1, target_person=self.p3)
            graph.get_relationship(source_person=a1, target_person=self.p4)
            graph.get_relationship(source_person=self.p1, target_person=a1)
            graph.get_relationship(source_person=self.p2, target_person=a1)
            graph.get_relationship(source_person=self.p3, target_person=a1)
            graph.get_relationship(source_person=self.p4, target_person=a1)

    def test_subgraph_edge_count_parent(self):
        n1_subgraph = self.p1.get_graph()
        c1 = graph.count_relationship_weights(self.p1, n1_subgraph)
        self.assertEqual(c1.get(1), 1)
        self.assertIsNone(c1.get(2))
        self.assertEqual(c1.get(3), 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child(self):
        n3_subgraph = self.p3.get_graph()
        c3 = graph.count_relationship_weights(self.p3, n3_subgraph)
        self.assertIsNone(c3.get(1))
        self.assertEqual(c3.get(2), 1)
        self.assertIsNone(c3.get(3))
        self.assertEqual(c3.get(4), 2)

    def test_subgraph_edge_count_parent_in_law(self):
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
        self.p3.get_or_create_relationship(a1, 1)
        n1_subgraph = self.p1.get_graph()
        c1 = graph.count_relationship_weights(self.p1, n1_subgraph)
        self.assertEqual(c1.get(1), 2)
        self.assertIsNone(c1.get(2))
        self.assertEqual(c1.get(3), 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child_in_law(self):
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
        self.p3.get_or_create_relationship(a1, 1)
        a1_subgraph = a1.get_graph()
        c4 = graph.count_relationship_weights(a1, a1_subgraph)
        self.assertEqual(c4.get(1), 1)
        self.assertEqual(c4.get(2), 1)
        self.assertIsNone(c4.get(3))
        self.assertEqual(c4.get(4), 2)

    def test_subgraph_edge_count_grandchild(self):
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
        relative = fake.family_member(sex='Male')
        a2 = Person(
            first_name=relative['first_name'],
            last_name=relative['last_name'],
            ethnic_name=relative['ethnic_name'],
            sex=relative['sex'],
            birth_date=relative['birth_date'],
            email=relative['email'],
            confirmed=False
        )
        db.session.add_all([a1, a2])
        db.session.commit()
        self.p3.get_or_create_relationship(a1, 1)
        self.p3.get_or_create_relationship(a2, 3)
        a1.get_or_create_relationship(a2, 3)
        a2_subgraph = a2.get_graph()
        c5 = graph.count_relationship_weights(a2, a2_subgraph)
        self.assertIsNone(c5.get(1))
        self.assertEqual(c5.get(2), 1)
        self.assertIsNone(c5.get(3))
        self.assertEqual(c5.get(4), 4)

    def test_subgraph_edge_count_grandparent(self):
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
        relative = fake.family_member(sex='Male')
        a2 = Person(
            first_name=relative['first_name'],
            last_name=relative['last_name'],
            ethnic_name=relative['ethnic_name'],
            sex=relative['sex'],
            birth_date=relative['birth_date'],
            email=relative['email'],
            confirmed=False
        )
        db.session.add_all([a1, a2])
        db.session.commit()
        self.p3.get_or_create_relationship(a1, 1)
        self.p3.get_or_create_relationship(a2, 3)
        a1.get_or_create_relationship(a2, 3)
        n1_subgraph = self.p1.get_graph()
        c6 = graph.count_relationship_weights(self.p1, n1_subgraph)
        self.assertEqual(c6.get(1), 2)
        self.assertIsNone(c6.get(2))
        self.assertEqual(c6.get(3), 3)
        self.assertIsNone(c6.get(4))

    def test_subgraph_edge_node_count_with_one_layer_and_size_3(self):
        self.reset()
        forge.run(units=1, size=3, layers=1, verbose=False)
        p1_graph = self.p1.get_graph()
        self.assertEqual(p1_graph.number_of_nodes(), 9)
        self.assertEqual(p1_graph.number_of_edges(), 8)

    def test_subgraph_edge_node_count_with_one_layer_and_size_4(self):
        self.reset()
        forge.run(units=1, size=4, layers=1, verbose=False)
        p1_graph = self.p1.get_graph()
        self.assertEqual(p1_graph.number_of_nodes(), 16)
        self.assertEqual(p1_graph.number_of_edges(), 15)

    def test_subgraph_edge_node_count_with_one_layer_and_size_5(self):
        self.reset()
        forge.run(units=1, size=5, layers=1, verbose=False)
        p1_graph = self.p1.get_graph()
        self.assertEqual(p1_graph.number_of_nodes(), 25)
        self.assertEqual(p1_graph.number_of_edges(), 24)
