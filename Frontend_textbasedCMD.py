# ----------------- Setup -----------------
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from heapq import heappush, heappop
from math import inf

# ----------------- Union-Find by Size -----------------
class UF_by_size:
    def __init__(self):
        self.id = {}
        self.set_member_cnt = defaultdict(lambda: 1)

    def check_same_union(self, u, v):
        return self.find(u) == self.find(v)

    def union(self, u, v):
        i = self.find(u)
        j = self.find(v)
        if i == j:
            return
        if self.set_member_cnt[i] > self.set_member_cnt[j]:
            i, j = j, i
        self.set_member_cnt[j] += self.set_member_cnt[i]
        del self.set_member_cnt[i]
        self.id[i] = j

    def find(self, up):
        while up in self.id and up != (deep := self.id[up]):
            self.id[up] = up = self.id[deep] if deep in self.id else deep
        return up

# ----------------- Bidirectional Dijkstra -----------------
class Bidirectional_Dijkstra:
    def __init__(self):
        self.adj_matrix = defaultdict(lambda: defaultdict(lambda: inf))

    def add_edge(self, n1, n2, weight):
        self.adj_matrix[n1][n2] = weight
        self.adj_matrix[n2][n1] = weight

    def check_data(self, people):
        return len(self.adj_matrix[people]) > 0

    def other_dir(self, dir):
        return 1 - dir

    def find_min_path(self, start_fri, target_fri):
        if start_fri == target_fri:
            return (0, [start_fri])
        seen = [set(), set()]
        dists = [{start_fri: 0}, {target_fri: 0}]
        paths = [{start_fri: [start_fri]}, {target_fri: [target_fri]}]
        node_heap = [(0, start_fri, 0), (0, target_fri, 1)]
        min_dist = inf
        min_path = []
        while node_heap:
            now_dist, now_fri, direct = heappop(node_heap)
            if now_dist > dists[direct][now_fri]:
                continue
            if now_fri in seen[self.other_dir(direct)]:
                break
            seen[direct].add(now_fri)
            for new_fri, new_weight in self.adj_matrix[now_fri].items():
                new_dist = now_dist + new_weight
                if new_dist < dists[direct].get(new_fri, inf):
                    dists[direct][new_fri] = new_dist
                    heappush(node_heap, (new_dist, new_fri, direct))
                    paths[direct][new_fri] = paths[direct][now_fri] + [new_fri]
                    if new_fri in dists[0] and new_fri in dists[1]:
                        totaldist = dists[0][new_fri] + dists[1][new_fri]
                        if min_dist > totaldist:
                            min_dist = totaldist
                            min_path = paths[0][new_fri][:-1] + paths[1][new_fri][::-1]
        if min_dist == inf:
            return (None, None)
        return min_dist, min_path

    def Dijkstra(self, start, target, limitation=inf):
        min_path = defaultdict(lambda: inf)
        min_path[start] = 0
        heap = [(0, start)]
        while heap:
            now_path, now_node = heappop(heap)
            if now_path > min_path[now_node]:
                continue
            if now_path > limitation or now_node == target:
                break
            for nei_node, nei_w in self.adj_matrix[now_node].items():
                if (new_path := now_path + nei_w) < min_path[nei_node]:
                    min_path[nei_node] = new_path
                    heappush(heap, (new_path, nei_node))
        return min_path[target]

# ----------------- Backend -----------------
class Backend:
    def init_space(self):
        self.uf = UF_by_size()
        self.graph = Bidirectional_Dijkstra()

    def __init__(self):
        self.init_space()

    def add_relation(self, fri1, fri2, connection_score):
        self.uf.union(fri1, fri2)
        self.graph.add_edge(fri1, fri2, connection_score)

    def check_relation(self, fri1, fri2):
        if self.graph.check_data(fri1) and self.graph.check_data(fri2):
            return self.uf.check_same_union(fri1, fri2)
        return False

    def get_best_path(self, fri1, fri2):
        if not self.check_relation(fri1, fri2):
            return (None, None)
        ret = self.graph.find_min_path(fri1, fri2)
        check = self.graph.Dijkstra(fri1, fri2)
        if check == inf:
            if ret[0] is not None:
                raise Exception("Mismatch in Dijkstra results")
        elif ret[0] != check:
            print(check, ret)
            raise Exception("Mismatch in Dijkstra results")
        return ret

    def visualize_graph(self, highlight_path=None):
        G = nx.Graph()
        for node, neighbors in self.graph.adj_matrix.items():
            for neigh, weight in neighbors.items():
                G.add_edge(node, neigh, weight=weight)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        if highlight_path:
            edges_in_path = list(zip(highlight_path, highlight_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=3)

        plt.show(block=False)  # non-blocking display
        plt.pause(0.1)

# ----------------- Interactive Menu -----------------
backend = Backend()

def frontend():
    while True:
        print("Please pick from the following options:")
        print("1: Add a connection")
        print("2: Check if there is a connection")
        print("3: Find best path to friendship")
        print("4: View friendship graph")
        print("5: Exit Program")

        choice = input("Please enter an option from above: ").strip()

        if choice == "1":
            fri1 = input("Please enter friend 1's name: ").strip()
            fri2 = input("Please enter friend 2's name: ").strip()
            try:
                score = int(input("Please enter your friendship score"))
            except ValueError:
                print("You must enter an integer")
                continue
            backend.add_relation(fri1, fri2, score)
            print(f"Success! Friendship between {fri1} and {fri2} added to graph!")

        elif choice == "2":
            fri1 = input("Please enter friend 1's name: ").strip()
            fri2 = input("Please enter friend 2's name: ").strip()
            connection = backend.check_relation(fri1, fri2)
            if connection:
                print(f"{fri1} and {fri2} are friends!")
            else:
                print(f"{fri1} and {fri2} are not friends!")

        elif choice == "3":
            fri1 = input("Please enter friend 1's name: ").strip()
            fri2 = input("Please enter friend 2's name: ").strip()
            distance, path = backend.get_best_path(fri1, fri2)
            if path is None:
                print(f"{fri1} and {fri2} have no mutual connection friendships!")
            else:
                print("The best path: " + "->".join(path))
                backend.visualize_graph(highlight_path=path)

        elif choice == "4":
            backend.visualize_graph()
        elif choice == "5":
            print("Thank you for using friend finder!")
            break
        else:
            print("Please choose from the options listed!")

frontend()

