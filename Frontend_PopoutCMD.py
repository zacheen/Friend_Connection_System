import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from collections import defaultdict
from heapq import heappush, heappop
from math import inf

# ----------------- Union-Find -----------------
class UF_by_size:
    def __init__(self):
        self.id = {}
        self.set_member_cnt = defaultdict(lambda: 1)

    def check_same_union(self, u, v):
        i = self.find(u)
        j = self.find(v)
        return i == j

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
        return (min_dist, min_path)

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
    def __init__(self, path=None):
        self.uf = UF_by_size()
        self.graph = Bidirectional_Dijkstra()
        if path:
            self.load_from_file(path)

    def load_from_file(self, path):
        with open(path, "r") as fr:
            while fr:
                input_line = fr.readline()
                if input_line == "-\n":
                    continue
                if input_line == "\n" or input_line == "":
                    break
                fri1, fri2, score = input_line.split(", ")
                score = int(score[:-1])
                self.add_relation(fri1, fri2, score)

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
                raise Exception
        elif ret[0] != check:
            print(check, ret)
            raise Exception
        return ret

# ----------------- GUI -----------------
class FriendshipGUI:
    def __init__(self, root_win):
        self.backend = Backend()
        self.root = root_win
        root_win.title("Friendship Network")
        root_win.geometry("1000x700")
        root_win.configure(bg="#f9f9f9")

        self.left_frame = tk.Frame(root_win, bg="#e8e8e8", padx=12, pady=12)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.left_frame, text="Friend Hub", font=("Arial", 24, "bold"), bg="#e8e8e8").pack(pady=10)

        tk.Label(self.left_frame, text="Person 1:", font=("Arial", 24), bg="#e8e8e8").pack(anchor='w')
        self.in1 = tk.Entry(self.left_frame, width=22, font=("Arial", 24))
        self.in1.pack(pady=3)

        tk.Label(self.left_frame, text="Person 2:", font=("Arial", 24), bg="#e8e8e8").pack(anchor='w')
        self.in2 = tk.Entry(self.left_frame, width=22, font=("Arial", 24))
        self.in2.pack(pady=3)

        tk.Label(self.left_frame, text="Score:", font=("Arial", 24), bg="#e8e8e8").pack(anchor='w')
        self.in_score = tk.Entry(self.left_frame, width=22, font=("Arial", 24))
        self.in_score.pack(pady=3)

        # buttons
        tk.Button(self.left_frame, text="Add Friend", command=self.add_friendship, bg="#808080", fg="white", width=20, font=("Arial", 24)).pack(pady=5)
        tk.Button(self.left_frame, text="Check Link", command=self.check_connection, bg="#808080", fg="white", width=20, font=("Arial", 24)).pack(pady=5)
        tk.Button(self.left_frame, text="Find Path", command=self.find_path, bg="#808080", fg="white", width=20, font=("Arial", 24)).pack(pady=5)
        tk.Button(self.left_frame, text="Show All", command=self.show_graph, bg="#808080", fg="white", width=20, font=("Arial", 24)).pack(pady=5)

        # status
        self.status = tk.Label(self.left_frame, text="", bg="#e8e8e8", fg="black", wraplength=220, justify="left", font=("Arial", 24))
        self.status.pack(pady=8)

        # right panel - graph
        self.fig, self.ax = plt.subplots(figsize=(7,7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root_win)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def draw_graph(self, highlight=None):
        self.ax.clear()
        G = nx.Graph()
        for n, neighs in self.backend.graph.adj_matrix.items():
            for m, w in neighs.items():
                G.add_edge(n, m, weight=w)
        pos = nx.spring_layout(G, seed=0)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, ax=self.ax, with_labels=True,
                node_color='#ffd699', node_size=900,
                font_size=12, font_weight='bold', edgecolors='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_size=11)

        if highlight:
            edges = list(zip(highlight, highlight[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3, ax=self.ax)

        self.canvas.draw()

    def add_friendship(self):
        a = self.in1.get().strip()
        b = self.in2.get().strip()
        try:
            score = int(self.in_score.get())
        except:
            self.status.config(text="Score must be a number", fg="red")
            return
        if a and b:
            self.backend.add_relation(a, b, score)
            self.status.config(text=f"Added: {a} <-> {b} ({score})", fg="green")
            self.draw_graph()
        else:
            self.status.config(text="Both names needed", fg="red")

    def check_connection(self):
        a = self.in1.get().strip()
        b = self.in2.get().strip()
        if a and b:
            con = self.backend.check_relation(a, b)
            self.status.config(text=f"Connected? {con}", fg="blue")
        else:
            self.status.config(text="Both names needed", fg="red")

    def find_path(self):
        a = self.in1.get().strip()
        b = self.in2.get().strip()
        if a and b:
            dist, path = self.backend.get_best_path(a, b)
            if path is None:
                self.status.config(text=f"No path between {a} and {b}", fg="red")
            else:
                self.status.config(text=f"Path: {' -> '.join(path)} (score {dist})", fg="purple")
                self.draw_graph(highlight=path)
        else:
            self.status.config(text="Both names needed", fg="red")

    def show_graph(self):
        self.draw_graph()
        self.status.config(text="Full graph shown", fg="black")


# ----------------- Run GUI -----------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = FriendshipGUI(root)
    root.mainloop()

