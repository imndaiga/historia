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

    def get_relationship(self, source_id, target_id):
        search_weight = self.GlobalGraph[source_id][target_id][source_id][
            'weight']
        return self.Relations.all_types[search_weight]

    def get_subgraph_from_person(self, person):
        edge_list = []
        processed_nodes = []
        target_id = person.id
        subgraph = nx.Graph()

        queue = [
            (u, v, w)
            for u, v, w in self.GlobalGraph.edges(data='weight')
            if u == target_id
        ]

        if self.GlobalGraph.has_node(person.id):
            for u, v, w in queue:
                processed_nodes.append(target_id)
                edge_list.extend(self._get_neighbours(target_id, queue))

                target_id = v
                queue.extend([
                    (new_u, new_v, new_w)
                    for new_u, new_v, new_w in
                    self.GlobalGraph.edges(data='weight')
                    if target_id in [new_u, new_v] and
                    new_v not in processed_nodes and
                    new_u not in processed_nodes
                ])
        subgraph.add_weighted_edges_from(edge_list)

        return subgraph

    @staticmethod
    def count_relationship_weights(source_id, graph):
        count = {}
        for node in graph.nodes():
            node_neighbors = graph.neighbors(node)
            for neighbor in node_neighbors:
                weight = graph[node][neighbor]['weight']

                if count.get(weight):
                    count[weight] = count.get(weight) + 1
                else:
                    count.setdefault(weight, 0)

        return count

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
