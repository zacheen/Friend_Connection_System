import json
from pathlib import Path

from Algorithm import *

class Backend:
    def init_space(self):
        self.uf = UF_by_size()
        self.graph = Bidirectional_Dijkstra()
    
    def __init__(self, path):
        self.init_space()
        if not path:
            return
        data_path = Path(path)
        if not data_path.exists():
            raise FileNotFoundError(f"Friendship data file not found: {path}")
        if data_path.suffix.lower() == ".json":
            self._load_from_json(data_path)
        else:
            self._load_from_legacy_text(data_path)

    def _load_from_json(self, data_path: Path):
        with data_path.open("r", encoding="utf-8") as fr:
            data = json.load(fr)
        relations = data.get("relations", [])
        for relation in relations:
            fri1 = relation.get("friend1")
            fri2 = relation.get("friend2")
            score = relation.get("score")
            if not fri1 or not fri2 or score is None:
                continue
            self.add_relation(fri1, fri2, int(score))

    def _load_from_legacy_text(self, data_path: Path):
        with data_path.open("r", encoding="utf-8") as fr:
            while True:
                input_line = fr.readline()
                if input_line == "-\n":
                    continue
                if input_line == "\n" or input_line == "":
                    break

                fri1, fri2, score = input_line.split(", ")
                score = int(score[:-1])
                self.add_relation(fri1, fri2, score)

    # def __init__(self, relation):
    #     self.init_space()
    #     for fri1, fri2, score in relation :
    #         self.add_relation(fri1, fri2, score)

    def set_limitation(self, limit):
        if limit == 0 :
            self.graph.set_limitation(inf)
        self.graph.set_limitation(limit)

    def add_relation(self, fri1, fri2, connection_score):
        self.uf.union(fri1, fri2)
        self.graph.add_edge(fri1, fri2, connection_score)

    def check_relation(self, fri1, fri2):
        if self.graph.check_data(fri1) and self.graph.check_data(fri2):
            return self.uf.check_same_union(fri1, fri2)
        return False

    # three posible return values:
    # 1. (path_len, path_list) : found the best path
    # 2. (None, ) : no connection
    # 3. (None, []) : the path is too long (exceed limitation)
    def get_best_path(self, fri1, fri2):
        if not self.check_relation(fri1, fri2) :
            return (None, None)
        ret = self.graph.find_min_path(fri1, fri2)
        check = self.graph.Dijkstra(fri1, fri2)
        if check == inf :
            if ret[0] != None :
                raise Exception
        elif ret[0] != check :
            print(check, ret)
            raise Exception
        return ret
    
    def find_target(self, start, target):
        return self.graph.Dijkstra(start, target)
    
    def get_all_nodes(self):
        """Get all unique nodes in the graph"""
        nodes = set()
        for node in self.graph.adj_matrix.keys():
            nodes.add(node)
            for neighbor in self.graph.adj_matrix[node].keys():
                nodes.add(neighbor)
        return list(nodes)
    
    def get_all_edges(self):
        """Get all edges with their weights"""
        edges = []
        seen = set()
        for node1 in self.graph.adj_matrix:
            for node2, weight in self.graph.adj_matrix[node1].items():
                edge_tuple = tuple(sorted([node1, node2]))
                if edge_tuple not in seen:
                    seen.add(edge_tuple)
                    edges.append({
                        'source': node1,
                        'target': node2,
                        'weight': weight
                    })
        return edges
    
    def get_graph_data(self):
        """Get complete graph data for visualization"""
        return {
            'nodes': [{'id': node, 'label': node} for node in self.get_all_nodes()],
            'edges': self.get_all_edges()
        }
    
    def get_connected_components(self):
        """Get all connected components in the graph"""
        components = defaultdict(set)
        for node in self.get_all_nodes():
            root = self.uf.find(node)
            components[root].add(node)
        return [list(component) for component in components.values()]

if __name__ == "__main__":
    pass
