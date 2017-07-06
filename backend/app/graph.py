import networkx as nx
import os


class Graph:

    def init_app(self, app):
        from app.models import Link, Relations
        self.gpickle_path = app.config['GRAPH_PATH']
        self.Link = Link
        self.Relations = Relations
        self.GlobalGraph = self._get_or_create_global_graph()

    def update(self):
        all_links = self.Link.query.all()
        self.add_relationship(all_links)
        nx.write_gpickle(self.GlobalGraph, self.gpickle_path)

    def add_relationship(self, relationship):
        for link in relationship:
            self.GlobalGraph.add_edge(
                link.ancestor_id,
                link.descendant_id,
                key=link.ancestor_id,
                weight=link.weight
            )

    def get_relationship(self, source_person, target_person):
        weight_list = self.all_relationship_weights(
            source_person)[target_person.id]

        if len(weight_list) < 2:
            return self.Relations.all_types[weight_list[0]]
        else:
            raise NotImplementedError(
                'Multi-step relationship analysis not implemented!'
            )

    def get_subgraph_from_person(self, source_person, span_type='maze'):
        '''
        Returns an nx.Graph object containing all nodes connected to
        source_person. Span_type parameter [maze, star, tree] dictates the
        algorithm used to move across the GlobalGraph.
        '''
        ebunch = []
        processed_nodes = []
        subgraph = nx.Graph()

        if span_type == 'maze':
            queue = [
                (u, v, w)
                for u, v, w in self.GlobalGraph.edges(data='weight')
                if u == source_person.id
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
            subgraph.add_weighted_edges_from(ebunch)

        if span_type == 'star':
            dijkstra_path_lengths = nx.single_source_dijkstra_path_length(
                self.GlobalGraph, source_person.id
            )

            subgraph.add_weighted_edges_from([
                (source_person.id, v, w)
                for v, w in dijkstra_path_lengths.items()
            ])

        if span_type == 'tree':
            raise NotImplementedError(
                'Tree spanning has not been implemented!'
            )

        return subgraph

    def all_relationship_weights(self, source_person):
        connections = {}

        lengths, paths = nx.single_source_dijkstra(
            source_person.get_graph(), source_person.id
        )
        del paths[source_person.id]

        for target in paths:
            if len(paths[target]) < 3:
                connections[target] = [lengths[target]]
            else:
                connections[target] = []
                for index, node in enumerate(paths[target]):
                    try:
                        next_node_in_path = paths[target][index + 1]

                        weight = self.GlobalGraph[
                            node][next_node_in_path][node]['weight']

                        connections[target].append(weight)
                    except IndexError:
                        pass

        return connections

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
