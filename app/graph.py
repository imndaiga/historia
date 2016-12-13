from .models import GlobalEdge, Relations
import networkx as nx
import os


class GlobalGraph:

    def __init__(self, app):
        self.gpickle_path = app.config['GRAPH_PATH']
        self.authorised = False
        if app.config['TESTING'] is True or app.config['DEBUG'] is True:
            self.authorised = True

    def update(self):
        G = self.current
        relation_links = GlobalEdge.query.all()
        for link in relation_links:
            source = link.ascendant_id
            target = link.descendant_id
            weight = link.edge_label
            key = link.ascendant_id
            if not G.has_edge(source, target, key=key):
                G.add_edge(source, target, key=key, weight=weight)
        self.save(G)

    def clear(self):
        if self.authorised:
            G = self.current
            G.clear()
            self.save(G)

    def get_subgraph(self, source, gtype=nx.Graph):
        subgraph = gtype()
        weighted_edge_list = self._resolve_edge_list_from_mdg(
            source=source,
            MDG=self.current)
        subgraph.add_weighted_edges_from(weighted_edge_list)
        return subgraph

    def _relations_list(self, source, target):
        relation_list = []
        weighted_edge_list = self._span_mdg(
            MDG=self.current, source=source, mutate=True).get(target.id)
        if weighted_edge_list:
            for edge_tuple in weighted_edge_list:
                (node_id, weight) = edge_tuple
                for relation in Relations['all_types']:
                    if weight == relation:
                        relation_list.append(
                            Relations['all_types'][relation])
            return relation_list
        else:
            return None

    def _resolve_edge_list_from_mdg(self, source, MDG):
        edges = []
        path_inputs = self._span_mdg(MDG=MDG, source=source)
        for node_id in path_inputs:
            set_node_id = None
            if len(path_inputs[node_id]) == 1:
                (_, weight_to_selfid) = path_inputs[node_id][0]
                edges.append((source.id, node_id, weight_to_selfid))
            elif len(path_inputs[node_id]) > 1:
                for path_tuples in path_inputs[node_id]:
                    if set_node_id is None:
                        (set_node_id, weight_to_selfid) = path_tuples
                    else:
                        (new_node_id, sum_weight) = path_tuples
                        new_weight = sum_weight - weight_to_selfid
                        edges.append((set_node_id, new_node_id, new_weight))
                        (set_node_id, weight_to_selfid) = path_tuples
        return edges

    def _span_mdg(self, MDG, source, mutate=False):
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
                                    list_of_edge_tuples=_selfid_to_uid_path)
                                ret_dict[u_id] = mut_paths
                            else:
                                ret_dict[u_id] = _selfid_to_uid_path
        return ret_dict

    @staticmethod
    def _mutate_to_sequential_paths(MDG, list_of_edge_tuples):
        ret_list = []
        prev_node_id = -99
        for half_edge in list_of_edge_tuples:
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

    @property
    def current(self):
        return self._load()

    def save(self, G):
        nx.write_gpickle(G, self.gpickle_path)

    def _load(self):
        if os.path.exists(self.gpickle_path):
            G = nx.read_gpickle(self.gpickle_path)
        else:
            G = nx.MultiDiGraph()
        return G
