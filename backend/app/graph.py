import networkx as nx
import os


class Graph:

    gpickle_path = None
    authorised = False

    Relations = {
        'directed_types': {
            3: ['Parent', 4], 4: ['Child', 3]},
        'undirected_types': {
            1: ['Partner'], 2: ['Sibling']},
        'all_types': {
            1: 'Partner', 2: 'Sibling', 3: 'Parent',
            4: 'Child', 5: 'Niece-Nephew', 6: 'Uncle-Aunt'},
        'modifiers': {
            1: 'Great', 2: 'Grand', 3: 'In-law'}
    }

    def init_app(self, app):
        from app.models import Link
        self.Link = Link
        self.gpickle_path = app.config['GRAPH_PATH']
        if app.config['TESTING'] is True or app.config['DEBUG'] is True:
            self.testing = True

    def update(self):
        G = self.current
        relation_links = self.Link.query.all()
        for link in relation_links:
            source = link.ascendant_id
            target = link.descendant_id
            weight = link.link_label
            key = link.ascendant_id
            if not G.has_edge(source, target, key=key):
                G.add_edge(source, target, key=key, weight=weight)
        self.save(G)

    def clear(self):
        if self.testing:
            G = self.current
            G.clear()
            self.save(G)

    def delete_node(self, node_id):
        G = self.current
        G.remove_node(node_id)
        self.save(G)

    def save(self, G):
        if self.gpickle_path is not None:
            nx.write_gpickle(G, self.gpickle_path)
        else:
            raise EnvironmentError

    def load_or_create(self):
        if self.gpickle_path is not None:
            if os.path.exists(self.gpickle_path):
                G = nx.read_gpickle(self.gpickle_path)
            else:
                G = nx.MultiDiGraph()
                self.save(G)
            return G
        else:
            raise EnvironmentError

    @property
    def current(self):
        return self.load_or_create()

    def get_subgraph(self, source, gtype=nx.Graph):
        subgraph = gtype()
        MDG = self.current
        if MDG.has_node(source.id):
            weighted_edge_list = self._resolve_edge_list_from_mdg(
                source=source,
                MDG=MDG)
            subgraph.add_weighted_edges_from(weighted_edge_list)
            return subgraph
        else:
            return nx.Graph()

    def span_mdg(self, MDG, source, mutate=False):
        '''
        Outputs a perspective-based adjacency list i.e. it traverses the
        provided multi-directed graph (MDG) selecting outbound edge weights
        from the source node. The mutate flag sequences the outputted
        path tuples.
        '''
        ret_dict = {}
        for u_id, nbrs in MDG.adjacency_iter():
            for v_id, keydict in nbrs.items():
                if u_id == source.id:
                    ret_dict[v_id] = list(
                        [(u_id, MDG[u_id][v_id][u_id]['weight'])])
                elif u_id != source.id and v_id != source.id:
                    if u_id not in ret_dict:
                        _selfid_to_uid_path = self._evaluate_path_in_mdg(
                            MDG=MDG,
                            source_id=source.id,
                            target_id=u_id)
                        if _selfid_to_uid_path is not None:
                            if mutate:
                                mut_paths = self._mutate_to_sequential_paths(
                                    MDG=MDG,
                                    path_tuples_list=_selfid_to_uid_path)
                                ret_dict[u_id] = mut_paths
                            else:
                                ret_dict[u_id] = _selfid_to_uid_path
        return ret_dict

    def get_relation_tree(self, source, target, readable=True):
        '''
        Outputs a list of outbound relations from the source
        to the target.
        '''
        relation_list = []
        MDG = self.current
        weighted_edge_list = self.span_mdg(
            MDG=MDG,
            source=source,
            mutate=True).get(target.id)
        if weighted_edge_list:
            for edge_tuple in weighted_edge_list:
                (node_id, weight) = edge_tuple
                for relation_key in self.Relations['all_types']:
                    if weight == relation_key:
                        if readable:
                            relation_list.append(
                                [
                                    self._getTreeNodeId(
                                        source, target, node_id),
                                    self.Relations['all_types'][relation_key]
                                ])
                        else:
                            relation_list.append(
                                [
                                    self._getTreeNodeId(
                                        source, target, node_id),
                                    relation_key
                                ])
            return relation_list
        else:
            return None

    @staticmethod
    def _getTreeNodeId(source, target, node_id):
        if source.id == node_id:
            return target.id
        else:
            return node_id

    def _resolve_edge_list_from_mdg(self, MDG, source):
        '''
        Outputs a computed ebunch list that can be added to a
        networkx graph using the nx.Graph.add_edges_from method.
        '''
        resolved_edges = []
        path_tuples_dict = self.span_mdg(MDG=MDG, source=source)
        for node_key in path_tuples_dict:
            set_node = None
            previous_weight = 0
            path_tuples_list = path_tuples_dict[node_key]
            if len(path_tuples_list) == 1:
                _, weight_from_source = path_tuples_list[0]
                new_path_tuple = (source.id, node_key, weight_from_source)
                resolved_edges.append(new_path_tuple)
            elif len(path_tuples_list) > 1:
                for path_tuple in path_tuples_list:
                    if set_node is None:
                        (set_node, previous_weight) = path_tuple
                    else:
                        (new_node, path_weight) = path_tuple
                        new_weight = path_weight - previous_weight
                        resolved_edges.append((set_node, new_node, new_weight))
                        (set_node, previous_weight) = path_tuple
        return resolved_edges

    @staticmethod
    def _mutate_to_sequential_paths(MDG, path_tuples_list):
        '''
        Takes a path tuples list and sequences it. The output is a list
        of 2-value tuples spanning the source_id to target_id path.
        Considering a path tuples list of length n, where i <= n. The first
        value of path_tuples_list[i] is a path node and the second is the
        djikstra graph weight of the previous path node in
        path_tuples_list[i-1] to the current path node in path_tuples_list[i].
        e.g.
            [(path_node_1, dijkstra_weight_of_source_id_to_path_node_1),
            (path_node_2, dijkstra_weight_of_path_node_1_to_path_node_2),
            (target_id, dijkstra_weight_of_path_node_2_to_target_id)]
        Note:
            A sequential path tuples list can be represented as a traditional
            path graph.
        '''
        ret_list = []
        prev_node_id = -99
        for half_edge in path_tuples_list:
            if prev_node_id == -99:
                (prev_node_id, _) = half_edge
                ret_list.append(half_edge)
            else:
                (new_node_id, _) = half_edge
                (weights, _) = nx.single_source_dijkstra(
                    MDG,
                    new_node_id,
                    prev_node_id,
                    weight='weight')
                target_weight = weights.get(prev_node_id)
                mut_half_edge = (new_node_id, target_weight)
                ret_list.append(mut_half_edge)
                (prev_node_id, _) = half_edge
        return ret_list

    @staticmethod
    def _evaluate_path_in_mdg(MDG, source_id, target_id):
        '''
        Returns a path tuples list i.e. a list of 2-value tuples spanning
        the source_id to target_id path. Considering a path tuples list of
        length n, where i <= n. The first value of path_tuples_list[i]
        is a path node and the second is the djikstra graph weight of
        the (source_id) to (path node) edge.
        e.g.
            [(path_node_1, dijkstra_weight_of_source_id_to_path_node_1),
            (path_node_2, dijkstra_weight_of_source_id_to_path_node_2),
            (target_id, dijkstra_weight_of_source_id_to_target_id)]
        Note:
            A path tuples list can be visually represented as a star graph
            with source_id being the central node.
        '''
        ret_list = []
        (weights, paths) = nx.single_source_dijkstra(
            MDG, source_id, target_id, weight='weight')
        target_path = paths.get(target_id)
        if target_path is not None:
            for node_id in target_path:
                if node_id != source_id:
                    ret_list.append((node_id, weights.get(node_id)))
            return ret_list
        else:
            return None

    @staticmethod
    def count_subgraph_weights(**kwargs):
        data = kwargs['data']
        counts = {}
        for edge in data:
            if counts.get(edge[2]['weight']):
                counts[edge[2]['weight']] = counts[edge[2]['weight']] + 1
            else:
                counts[edge[2]['weight']] = 1
        return counts
