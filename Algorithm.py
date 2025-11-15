from collections import defaultdict
class UF_by_size:
    def __init__(self):
        self.id = {}
        self.set_member_cnt = defaultdict(lambda : 1)

    def check_same_union(self, u, v):
        i = self.find(u)
        j = self.find(v)
        return i == j

    def union(self, u, v):
        i = self.find(u)
        j = self.find(v)
        if i == j:
            return
        # to minimize the adjust of find(), I union the smaller set into the bigger set
        if self.set_member_cnt[i] > self.set_member_cnt[j] :
            i,j = j,i
        self.set_member_cnt[j] += self.set_member_cnt[i]
        del(self.set_member_cnt[i])
        self.id[i] = j

    def find(self, up):
        while up in self.id and up != (deep := self.id[up]):
            self.id[up] = up = (self.id[deep] if deep in self.id else deep)
        return up
    
from heapq import heappush, heappop
from math import inf
# defaultdict version, so that we can add in any amount and any type of item
    # checked with "https://leetcode.com/problems/path-with-maximum-probability/description/"
class Bidirectional_Dijkstra:
    def __init__(self):
        self.weight_limitation = inf # result weight should be less than this value
        self.adj_matrix = defaultdict(lambda : defaultdict(lambda : inf))

    def set_limitation(self, limit):
        self.weight_limitation = limit

    def add_edge(self, n1, n2, weight):
        self.adj_matrix[n1][n2] = weight
        self.adj_matrix[n2][n1] = weight

    # check having any friends (if no friends, it is impossible to expand friendship)
    def check_data(self, people): 
        return len(self.adj_matrix[people]) > 0
    
    # return another direction
    # dir: 0 - Forward, 1 - Backward
    def other_dir(self, dir):
        return 1-dir

    def find_min_path(self, start_fri, target_fri):
        # Handle same person case
        if start_fri == target_fri:
            return (0, [start_fri])

        # using list to memorize both directions' info
        seen = [set(), set()]
        dists = [{start_fri: 0}, {target_fri: 0}]  # total distances from start and target node
        paths = [{start_fri: [start_fri]}, {target_fri: [target_fri]}]  # minimum weight paths to start and target node
        node_heap = [(0, start_fri, 0), (0, target_fri, 1)]  # heap of (distance, node, dir) for choosing next node to expand

        min_dist = inf
        min_path = []
        while node_heap:
            # get minimum distance to expand
            now_dist, now_fri, direct = heappop(node_heap)
            if now_dist > dists[direct][now_fri]:
                # Shortest path to now_fri has already been found
                continue
            if now_fri in seen[self.other_dir(direct)]:
                break
            seen[direct].add(now_fri)
            for new_fri, new_weight in self.adj_matrix[now_fri].items():
                new_dist = now_dist + new_weight
                if new_dist >= self.weight_limitation :
                    continue
                if new_dist < dists[direct].get(new_fri, inf):
                    dists[direct][new_fri] = new_dist
                    heappush(node_heap, (new_dist, new_fri, direct))
                    paths[direct][new_fri] = paths[direct][now_fri] + [new_fri]
                    if new_fri in dists[0] and new_fri in dists[1]: # if new_fri connects both sets
                        # check whether this path is better
                        totaldist = dists[0][new_fri] + dists[1][new_fri]
                        if totaldist < self.weight_limitation and min_dist > totaldist:
                            min_dist = totaldist
                            min_path = paths[0][new_fri][:-1] + paths[1][new_fri][::-1]
                            # since paths[0][new_fri][-1] == paths[1][new_fri][-1]
        if min_dist == inf:
            return (None, [])
        return (min_dist, min_path)
    
    # for testing # (Use this with find_min_path to verify the minimum weight path.)
        # if exceed limitation would return inf
    def Dijkstra(self, start, target):
        min_path = defaultdict(lambda : self.weight_limitation)
        min_path[start] = 0
        heap = [(0, start)]
        while heap:
            now_path, now_node = heappop(heap)
            if now_path > min_path[now_node] :
                continue
            if now_node == target:
                break
            # min_path[now_node] = now_path # no needed
            for nei_node, nei_w in self.adj_matrix[now_node].items() :
                if (new_path := now_path + nei_w) < min_path[nei_node] :
                    min_path[nei_node] = new_path
                    heappush(heap, (new_path, nei_node))
        if min_path[target] == self.weight_limitation :
            return inf
        return min_path[target]

if __name__ == "__main__":
    pass