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
        for link in all_links:
            self.GlobalGraph.add_weighted_edges_from([(
                link.ancestor_id,
                link.descendant_id,
                link.weight
            )])
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

    def get_subgraph_from_person(self, source_person):
        edge_list = []
        processed_nodes = []
        source_id = source_person.id
        subgraph = nx.Graph()

        queue = [
            (u, v, w)
            for u, v, w in self.GlobalGraph.edges(data='weight')
            if u == source_id
        ]

        if self.GlobalGraph.has_node(source_id):
            for u, v, w in queue:
                processed_nodes.append(source_id)
                edge_list.extend(self._get_neighbours(source_id, queue))

                source_id = v
                queue.extend([
                    (new_u, new_v, new_w)
                    for new_u, new_v, new_w in
                    self.GlobalGraph.edges(data='weight')
                    if source_id in [new_u, new_v] and
                    new_v not in processed_nodes and
                    new_u not in processed_nodes
                ])
        subgraph.add_weighted_edges_from(edge_list)

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
