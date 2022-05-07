import abc
from dsa1lib.graph import WeightedDirectedGraph, WeightedGraph


class AllPairShortestPathAlgo(abc.ABC):

    def __init__(self, graph: WeightedGraph):
        self.graph = graph
        self.shortest_dist_mat = [[float("inf") for _ in range(
            self.graph.num_vertices)] for _ in range(self.graph.num_vertices)]
        self.has_neg_cycle = False
        self._find_all_pair_shortest_path()

    @abc.abstractmethod
    def _find_all_pair_shortest_path(self):
        raise NotImplementedError()


class FloydWalshallAPSP(AllPairShortestPathAlgo):

    def __init__(self, graph: WeightedGraph):
        super().__init__(graph)

    def _find_all_pair_shortest_path(self):
        for i in range(self.graph.num_vertices):
            self.shortest_dist_mat[i][i] = 0

        for edge in self.graph.get_all_edges():
            from_v = edge.any_vertex()
            to_v = edge.other_vertex(from_v)
            self.shortest_dist_mat[from_v][to_v] = edge.weight

        for highest_v_idx in range(self.graph.num_vertices):
            for v1 in range(self.graph.num_vertices):
                for v2 in range(self.graph.num_vertices):
                    dist_using_highest_v = self.shortest_dist_mat[v1][highest_v_idx] + \
                        self.shortest_dist_mat[highest_v_idx][v2]

                    if dist_using_highest_v < self.shortest_dist_mat[v1][v2]:
                        # if v1 == v2:
                        #     print("negative cycle detected")
                        self.shortest_dist_mat[v1][v2] = dist_using_highest_v

        for i in range(self.graph.num_vertices):
            if self.shortest_dist_mat[i][i] < 0:
                self.has_neg_cycle = True


if __name__ == "__main__":
    V, E = [int(inp) for inp in input().split()]
    graph = WeightedDirectedGraph(V)

    for _ in range(E):
        v1, v2, w = input().split()
        v1, v2, w = int(v1) - 1, int(v2) - 1, float(w)
        graph.add_edge(v1, v2, w)

    floydwarshall = FloydWalshallAPSP(graph)

    def print_mat(mat: list[list]):
        for r in range(len(mat)):
            arr = mat[r]
            for c in range(len(arr)):
                print(f"{mat[r][c] : .2f}", "\t", end="")
            print()

    if not floydwarshall.has_neg_cycle:
        print("Shortest distance matrix")
        print_mat(floydwarshall.shortest_dist_mat)
    else:
        print("Negative Cycle Found")
