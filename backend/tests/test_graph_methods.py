import unittest
from app import create_app, db, graph, seed
from app.models import Person
from app.seed import fake
import os
import networkx as nx


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.reset()
        seed.run(family_units=1, family_size=4, layers=0, verbose=False)
        self.p1 = db.session.query(Person).filter_by(
            baptism_name='Patricia').first()
        self.p2 = db.session.query(Person).filter_by(
            baptism_name='Tina').first()
        self.p3 = db.session.query(Person).filter_by(
            baptism_name='Kerry').first()
        self.p4 = db.session.query(Person).filter_by(
            baptism_name='Paige').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def reset():
        db.session.remove()
        db.drop_all()
        db.create_all()
        graph.clear()
        seed.auto = True

    def delete_gpickle_file(self):
        if os.path.exists(self.app.config['GRAPH_PATH']):
            os.remove(self.app.config['GRAPH_PATH'])

    def test_graph_is_testing(self):
        self.assertTrue(graph.testing)
        self.assertTrue('graph-test.gpickle' in self.app.config['GRAPH_PATH'])

    def test_graph_load_with_invalid_environment_variable(self):
        graph.gpickle_path = None
        with self.assertRaises(EnvironmentError):
            graph._load()

    def test_graph_load_instatiates_gpickle_file(self):
        self.delete_gpickle_file()
        self.assertFalse(os.path.exists(self.app.config['GRAPH_PATH']))
        G = graph._load()
        self.assertTrue(os.path.exists(self.app.config['GRAPH_PATH']))
        self.assertEqual(G.order(), 0)
        self.assertEqual(G.size(), 0)

    def test_graph_load_is_successful(self):
        G = graph._load()
        self.assertEqual(G.order(), 4)
        self.assertEqual(G.size(), 12)

    def test_graph_save_with_invalid_environment_variable(self):
        graph.gpickle_path = None
        G = nx.MultiGraph()
        with self.assertRaises(EnvironmentError):
            graph.save(G)

    def test_graph_save_is_successful(self):
        self.delete_gpickle_file()
        self.assertFalse(os.path.exists(self.app.config['GRAPH_PATH']))
        G = nx.MultiGraph()
        graph.save(G)
        self.assertTrue(os.path.exists(self.app.config['GRAPH_PATH']))
        os.remove(self.app.config['GRAPH_PATH'])

    def test_graph_update_is_successful(self):
        self.delete_gpickle_file()
        G = graph.current
        self.assertEqual(G.order(), 0)
        self.assertEqual(G.size(), 0)
        graph.update()
        G = graph.current
        self.assertEqual(G.order(), 4)
        self.assertEqual(G.size(), 12)

    def test_graph_clear_is_successful(self):
        graph.clear()
        G = graph.current
        self.assertEqual(G.order(), 0)
        self.assertEqual(G.size(), 0)

    def test_graph_has_no_selfloops(self):
        G = graph.current
        self.assertEqual(G.number_of_selfloops(), 0)

    def test_graph_get_subgraph_is_successful(self):
        n1_subgraph = graph.get_subgraph(source=self.p1)
        self.assertEqual(n1_subgraph.number_of_edges(), 3)
        self.assertEqual(n1_subgraph.number_of_nodes(), 4)

    def test_subgraph_basic_relations(self):
        n1_n2_relation = graph.get_relation_tree(
            source=self.p1, target=self.p2)
        n1_n3_relation = graph.get_relation_tree(
            source=self.p1, target=self.p3)
        n1_n4_relation = graph.get_relation_tree(
            source=self.p1, target=self.p4)
        n2_n1_relation = graph.get_relation_tree(
            source=self.p2, target=self.p1)
        n2_n3_relation = graph.get_relation_tree(
            source=self.p2, target=self.p3)
        n2_n4_relation = graph.get_relation_tree(
            source=self.p2, target=self.p4)
        n3_n1_relation = graph.get_relation_tree(
            source=self.p3, target=self.p1)
        n3_n2_relation = graph.get_relation_tree(
            source=self.p3, target=self.p2)
        n3_n4_relation = graph.get_relation_tree(
            source=self.p3, target=self.p4)
        n4_n1_relation = graph.get_relation_tree(
            source=self.p4, target=self.p1)
        n4_n2_relation = graph.get_relation_tree(
            source=self.p4, target=self.p2)
        n4_n3_relation = graph.get_relation_tree(
            source=self.p4, target=self.p3)
        self.assertEqual(n1_n2_relation[0][1], 'Partner')
        self.assertEqual(n1_n3_relation[0][1], 'Parent')
        self.assertEqual(n1_n4_relation[0][1], 'Parent')
        self.assertEqual(n2_n1_relation[0][1], 'Partner')
        self.assertEqual(n2_n3_relation[0][1], 'Parent')
        self.assertEqual(n2_n4_relation[0][1], 'Parent')
        self.assertEqual(n3_n1_relation[0][1], 'Child')
        self.assertEqual(n3_n2_relation[0][1], 'Child')
        self.assertEqual(n3_n4_relation[0][1], 'Sibling')
        self.assertEqual(n4_n1_relation[0][1], 'Child')
        self.assertEqual(n4_n2_relation[0][1], 'Child')
        self.assertEqual(n4_n3_relation[0][1], 'Sibling')

    def test_subgraph_null_relations(self):
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
        with self.assertRaises(KeyError):
            graph.get_relation_tree(source=a1, target=self.p1)
            graph.get_relation_tree(source=a1, target=self.p2)
            graph.get_relation_tree(source=a1, target=self.p3)
            graph.get_relation_tree(source=a1, target=self.p4)
            graph.get_relation_tree(source=self.p1, target=a1)
            graph.get_relation_tree(source=self.p2, target=a1)
            graph.get_relation_tree(source=self.p3, target=a1)
            graph.get_relation_tree(source=self.p4, target=a1)

    def test_subgraph_edge_count_parent(self):
        n1_subgraph = graph.get_subgraph(source=self.p1)
        data = n1_subgraph.edges(data=True)
        c1 = graph.count_subgraph_weights(data=data)
        self.assertEqual(c1.get(1), 1)
        self.assertIsNone(c1.get(2))
        self.assertEqual(c1.get(3), 2)
        self.assertIsNone(c1.get(4))

    def test_subgraph_edge_count_child(self):
        n3_subgraph = graph.get_subgraph(source=self.p3)
        data = n3_subgraph.edges(data=True)
        c2 = graph.count_subgraph_weights(data=data)
        self.assertIsNone(c2.get(1))
        self.assertEqual(c2.get(2), 1)
        self.assertIsNone(c2.get(3))
        self.assertEqual(c2.get(4), 2)

    def test_subgraph_edge_count_parent_in_law(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(partners=[self.p3, a1])
        graph.update()
        n1_subgraph = graph.get_subgraph(source=self.p1)
        data = n1_subgraph.edges(data=True)
        c3 = graph.count_subgraph_weights(data=data)
        self.assertEqual(c3.get(1), 2)
        self.assertIsNone(c3.get(2))
        self.assertEqual(c3.get(3), 2)
        self.assertIsNone(c3.get(4))

    def test_subgraph_edge_count_child_in_law(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(partners=[self.p3, a1])
        graph.update()
        a1_subgraph = graph.get_subgraph(source=a1)
        data = a1_subgraph.edges(data=True)
        c4 = graph.count_subgraph_weights(data=data)
        self.assertEqual(c4.get(1), 1)
        self.assertEqual(c4.get(2), 1)
        self.assertIsNone(c4.get(3))
        self.assertEqual(c4.get(4), 2)

    def test_subgraph_edge_count_grandchild(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        relative = fake.family_member(sex='M')
        a2 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(parents=[self.p3, a1], children=[a2])
        graph.update()
        a2_subgraph = graph.get_subgraph(source=a2)
        data = a2_subgraph.edges(data=True)
        c5 = graph.count_subgraph_weights(data=data)
        self.assertIsNone(c5.get(1))
        self.assertEqual(c5.get(2), 1)
        self.assertIsNone(c5.get(3))
        self.assertEqual(c5.get(4), 4)

    def test_subgraph_edge_count_grandparent(self):
        relative = fake.family_member(sex='F')
        a1 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        relative = fake.family_member(sex='M')
        a2 = Person(
            baptism_name=relative['name'].split()[0],
            surname=relative['name'].split()[1],
            sex=relative['sex'],
            dob=relative['birthdate'],
            email=relative['mail'],
            confirmed=True
        )
        seed.relate(parents=[self.p3, a1], children=[a2])
        graph.update()
        n1_subgraph = graph.get_subgraph(source=self.p1)
        data = n1_subgraph.edges(data=True)
        c6 = graph.count_subgraph_weights(data=data)
        self.assertEqual(c6.get(1), 2)
        self.assertIsNone(c6.get(2))
        self.assertEqual(c6.get(3), 3)
        self.assertIsNone(c6.get(4))

    def test_subgraph_edge_node_count_with_one_layer_and_family_size_3(self):
        self.reset()
        seed.run(family_units=1, family_size=3, layers=1, verbose=False)
        p1_graph = graph.get_subgraph(self.p1)
        self.assertEqual(p1_graph.number_of_nodes(), 9)
        self.assertEqual(p1_graph.number_of_edges(), 8)

    def test_subgraph_edge_node_count_with_one_layer_and_family_size_4(self):
        self.reset()
        seed.run(family_units=1, family_size=4, layers=1, verbose=False)
        p1_graph = graph.get_subgraph(self.p1)
        self.assertEqual(p1_graph.number_of_nodes(), 16)
        self.assertEqual(p1_graph.number_of_edges(), 15)

    def test_subgraph_edge_node_count_with_one_layer_and_family_size_5(self):
        self.reset()
        seed.run(family_units=1, family_size=5, layers=1, verbose=False)
        p1_graph = graph.get_subgraph(self.p1)
        self.assertEqual(p1_graph.number_of_nodes(), 25)
        self.assertEqual(p1_graph.number_of_edges(), 24)
