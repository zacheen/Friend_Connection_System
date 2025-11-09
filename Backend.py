from Algorithm import *

class Backend:
    def init_space(self):
        self.uf = UF_by_size()
        self.graph = Bidirectional_Dijkstra()
    
    def __init__(self, path):
        self.init_space()
        with open(path, "r") as fr :
            while fr :
                # deal with data
                input_line = fr.readline()
                if input_line == "-\n" :
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

    def add_relation(self, fri1, fri2, connection_score):
        self.uf.union(fri1, fri2)
        self.graph.add_edge(fri1, fri2, connection_score)

    def check_relation(self, fri1, fri2):
        if self.graph.check_data(fri1) and self.graph.check_data(fri2):
            return self.uf.check_same_union(fri1, fri2)
        return False

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

if __name__ == "__main__":
    pass