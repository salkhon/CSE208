import math
from typing import cast
from graph import WeightedUndirectedEdge, WeightedUndirectedGraph
from indexheap import IndexedMinPQ
from unionfind import UnionFind


class MSTAlgorithm:
    def __init__(self, graph: WeightedUndirectedGraph):
        self.graph = graph
        self.edge_to = [None] * self.graph.num_vertices
        # will store edge_to each vertex
        self.predecessor = [None] * self.graph.num_vertices
        self.mst = self._find_mst()

    def _find_mst(self) -> list[WeightedUndirectedEdge]:
        raise NotImplementedError

    @property
    def mst_weight(self) -> float:
        weight = 0
        for edge in self.mst:
            weight += edge.weight
        return weight


class KruskalMST(MSTAlgorithm):
    def __init__(self, graph: WeightedUndirectedGraph):
        super().__init__(graph)

    def _find_mst(self) -> list[WeightedUndirectedEdge]:
        # cast can be ommited with covariance
        edges = cast(list[WeightedUndirectedEdge], self.graph.get_all_edges())
        edges.sort()

        uf = UnionFind(self.graph.num_vertices)

        mst = []

        for edge in edges:
            v1 = edge.any_vertex()
            v2 = edge.other_vertex(v1)
            if not uf.in_same_set(v1, v2):
                mst.append(edge)
                uf.union(v1, v2)

        return mst


class PrimMST(MSTAlgorithm):
    def __init__(self, graph: WeightedUndirectedGraph):
        super().__init__(graph)

    def _find_mst(self) -> list[WeightedUndirectedEdge]:
        self.predecessor: list = [None] * self.graph.num_vertices
        is_in_mst = [False] * self.graph.num_vertices

        indexed_min_pq = IndexedMinPQ(max_len=self.graph.num_vertices)

        def visit(edge: WeightedUndirectedEdge | None, to_vertex: int):
            self.predecessor[to_vertex] = edge
            is_in_mst[to_vertex] = True

            for adj_edge in self.graph.adj(to_vertex):
                adj_edge = cast(WeightedUndirectedEdge, adj_edge)
                neighbor_vertex = adj_edge.other_vertex(to_vertex)

                if not is_in_mst[neighbor_vertex]:
                    if not indexed_min_pq.key_of_index(neighbor_vertex):
                        indexed_min_pq.insert(neighbor_vertex, adj_edge)
                    elif adj_edge < indexed_min_pq.key_of_index(neighbor_vertex):
                        indexed_min_pq.decrease_key(neighbor_vertex, adj_edge)

        visit(None, 0)

        while len(indexed_min_pq):
            to_vertex, next_min_edge = indexed_min_pq.del_min()

            if not is_in_mst[to_vertex]:
                visit(next_min_edge, to_vertex)

        return self._gather_mst()

    def _gather_mst(self) -> list[WeightedUndirectedEdge]:
        mst: list[WeightedUndirectedEdge] = []
        for v in range(self.graph.num_vertices):
            if self.predecessor[v]:
                print(v, self.predecessor[v])
                mst.append(self.predecessor[v])
        return mst


if __name__ == "__main__":
    V, E = [int(inp) for inp in input().split()]
    graph = WeightedUndirectedGraph(V)

    for edge in range(E):
        v1, v2, w = input().split()
        graph.add_edge(int(v1), int(v2), float(w))

    kruskal = KruskalMST(graph)
    prim = PrimMST(graph)

    print("Cost of the minimum spanning tree :", prim.mst_weight)
    print("Cost of the minimum spanning tree :", kruskal.mst_weight)

    prim_edges = [(edge.any_vertex(), edge.other_vertex(
        edge.any_vertex())) for edge in prim.mst]
    kruskal_edges = [(edge.any_vertex(), edge.other_vertex(
        edge.any_vertex())) for edge in kruskal.mst]

    print("List of edges selected by Prim's:", prim_edges)
    print("List of edges selected by Kruskal's:", kruskal_edges)
