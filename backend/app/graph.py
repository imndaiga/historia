import networkx as nx
import os


class Graph:

    def init_app(self, app):
        from app.models import Person, Link
        from .utils import Relations

        self.gpickle_path = app.config['GRAPH_PATH']
        self.Link = Link
        self.Relations = Relations
        self.GlobalGraph = self._get_or_create_global_graph()
        self.Person = Person

    def update_edges(self):
        all_links = self.Link.query.all()
        for link in all_links:
            self.create_from_model_instance(link)
            self.create_from_model_instance(link.ancestor)
            self.create_from_model_instance(link.descendant)
        nx.write_gpickle(self.GlobalGraph, self.gpickle_path)

    def get_relationship(self, source_id, target_id):
        weight_list = self.all_relationship_weights(
            source_id)[target_id]

        if len(weight_list) < 2:
            return self.Relations.all_types[weight_list[0]]
        else:
            raise NotImplementedError(
                'Multi-step relationship analysis not implemented!'
            )

    def get_subgraph_from_id(self, source_id, span_type='tree'):
        '''
        Returns an nx.Graph object containing all nodes connected to
        source_id. Span_type parameter [maze, star, tree] dictates the
        algorithm used to move across the GlobalGraph.
        '''
        ebunch = []
        processed_nodes = []

        if span_type == 'maze':
            queue = [
                (u, v, w)
                for u, v, w in self.GlobalGraph.edges(data='weight')
                if u == source_id
            ]

            for u, v, w in queue:
                processed_nodes.append(u)
                ebunch.extend(self._get_neighbours(u, queue))

                queue.extend([
                    (new_u, new_v, new_w)
                    for new_u, new_v, new_w in
                    self.GlobalGraph.edges(data='weight')
                    if v == new_u and
                    new_v not in processed_nodes
                ])

        if span_type == 'star':
            dijkstra_path_lengths = nx.single_source_dijkstra_path_length(
                self.GlobalGraph, source_id
            )

            ebunch = [
                (source_id, v, w)
                for v, w in dijkstra_path_lengths.items()
            ]

        if span_type == 'tree':
            paths = nx.single_source_dijkstra_path(
                self.GlobalGraph, source_id
            )
            paths.pop(source_id)

            for target in paths:
                path_size = len(paths[target])
                for i in range(path_size):
                    if i + 1 < path_size:
                        u = paths[target][i]
                        v = paths[target][i + 1]
                        w = self.GlobalGraph[u][v][u]

                        ebunch.append((u, v, w))

        return self._create_digraph_from_ebunch(ebunch)

    def all_relationship_weights(self, source_id):
        connections = {}

        lengths, paths = nx.single_source_dijkstra(
            self.GlobalGraph, source_id
        )
        del paths[source_id]

        for target in paths:
            if len(paths[target]) < 3:
                connections[target] = [lengths[target]]
            else:
                connections[target] = []
                for index, node in enumerate(paths[target]):
                    if index + 1 < len(paths[target]):
                        next_node_in_path = paths[target][index + 1]

                        weight = self.GlobalGraph[
                            node][next_node_in_path][node]['weight']

                        connections[target].append(weight)

        return connections

    def create_from_model_instance(self, model):
        if isinstance(model, self.Person):
            self.GlobalGraph.add_node(
                model.id,
                {
                    'first_name': model.first_name,
                    'ethnic_name': model.ethnic_name,
                    'last_name': model.last_name,
                    'birth_date': model.birth_date,
                    'sex': model.sex,
                    'email': model.email
                }
            )
        if isinstance(model, self.Link):
            self.GlobalGraph.add_edge(
                model.ancestor_id,
                model.descendant_id,
                key=model.ancestor_id,
                weight=model.weight
            )

    def _create_digraph_from_ebunch(self, ebunch):
        g = nx.DiGraph()

        for edge in ebunch:
            (u, v, w) = edge
            u_data = self.GlobalGraph.node[u]
            v_data = self.GlobalGraph.node[v]
            g.add_nodes_from([(u, u_data), (v, v_data)])

        g.add_weighted_edges_from(ebunch)

        return g

    @staticmethod
    def _get_neighbours(target_id, ebunch):
        neighbours = []
        for u, v, w in ebunch:
            if u == target_id:
                neighbours.append((u, v, w))

        return neighbours

    def _get_or_create_global_graph(self):
        if os.path.exists(self.gpickle_path):
            return nx.read_gpickle(self.gpickle_path)
        else:
            GG = nx.MultiDiGraph()
            nx.write_gpickle(GG, self.gpickle_path)
            return GG
