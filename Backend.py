import json
from pathlib import Path

from Algorithm import *
from persona_data import PERSONAS, get_persona

class Backend:
    def init_space(self):
        self.uf = UF_by_size()
        self.graph = Bidirectional_Dijkstra()
        self.get_persona = get_persona
    
    def __init__(self, path):
        self.init_space()
        if not path:
            return
        self.data_path = Path(path)
        if not self.data_path.exists():
            raise FileNotFoundError(f"Friendship data file not found: {path}")
        if self.data_path.suffix.lower() == ".json":
            print("read relation from json file")
            self._load_from_json()
        else:
            self._load_from_legacy_text()
        self.save_data_path = self.data_path.with_name(self.data_path.name + "_new_data")
    
    def when_exit(self):
        self._save_to_json()

    def _load_from_json(self):
        with self.data_path.open("r", encoding="utf-8") as fr:
            data = json.load(fr)
        relations = data.get("relations", [])
        for info in relations:
            if len(info) != 3:
                continue
            fri1, fri2, score = info
            self.add_relation(fri1, fri2, int(score))
    
    def _load_from_legacy_text(self):
        with self.data_path.open("r", encoding="utf-8") as fr:
            while True:
                input_line = fr.readline()
                if input_line == "-\n":
                    continue
                if input_line == "\n" or input_line == "":
                    break

                fri1, fri2, score = input_line.split(", ")
                score = int(score[:-1])
                self.add_relation(fri1, fri2, score)

    def _dump_compact_list_json(self, data): # hardcode
        key = "relations"
        
        print("export_file:",str(self.save_data_path))
        
        with open(self.save_data_path, "w", encoding="utf8") as fw:
            # 開頭大括號
            fw.write("{\n")

            # 寫 key 與中括號開頭
            fw.write(f'  "{key}": [\n')

            # 逐行寫入內層 list 內容
            for i, item in enumerate(data[key]):
                line = "    " + json.dumps(item, ensure_ascii=False)
                if i != len(data) - 1:
                    line += ","
                fw.write(line + "\n")

            # 關閉中括號與大括號
            fw.write("  ]\n")
            fw.write("}\n")

    def _save_to_json(self):
        relations = []
        for fri1, fri2_info in self.graph.adj_matrix.items():
            for fri2, score in fri2_info.items():
                if fri1 < fri2:  # to avoid duplicates
                    relations.append([fri1, fri2, score])
        data = {"relations": relations}
        
        # # normal saving method
        # with save_data_path.open("w", encoding="utf-8") as fw:
        #     json.dump(data, fw, indent=4)
        # # for better readability
        self._dump_compact_list_json(data)

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
    # 2. (None, None) : no connection
    # 3. (None, []) : the path is too long (exceed limitation)
    def get_best_path(self, fri1, fri2):
        if not self.check_relation(fri1, fri2) :
            return (None, None)
        ret = self.graph.find_min_path(fri1, fri2)
        check = self.graph.Dijkstra(fri1, fri2)
        if ret[0] != check[0] :
            print(check, ret)
            raise Exception
        return ret
    
    # three posible return values:
    # 1. (path_len, path_list) : found the best path
    # 2. (None, None) : no connection
    def find_target(self, start, target):
        return self.graph.Dijkstra(start, target, find_info="summary", get_info=self.get_persona)
    
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
    backend = Backend('friendship_data.json')
    print(backend.get_best_path("Kevin", "Charlie"))
    # print(backend.find_target("Bob", "Google"))
