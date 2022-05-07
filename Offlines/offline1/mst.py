
from typing import cast
from dsa1lib.graph import WeightedUndirectedEdge, WeightedDirectedGraph, WeightedUndirectedGraph
import math
import heapq
from dsa1lib.unionfind import UnionFind


class MSTAlgorithm:
    def __init__(self, graph: WeightedUndirectedGraph):
        self.graph = graph
        self.edge_to = [None] * self.graph.num_vertices
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
        color = [0] * self.graph.num_vertices
        minpq = []
        mst = []

        def visit(edge: WeightedUndirectedEdge | None, to_vertex: int):
            color[to_vertex] = 1
            if edge:
                mst.append(edge)

            for adj_edge in self.graph.adj(to_vertex):
                adj_edge = cast(WeightedUndirectedEdge, adj_edge)
                other_v = adj_edge.other_vertex(to_vertex)
                if color[other_v] == 0:
                    heapq.heappush(minpq, adj_edge)

        visit(None, 0)
        while len(minpq):
            next_min_edge = heapq.heappop(minpq)
            v1 = next_min_edge.any_vertex()
            v2 = next_min_edge.other_vertex(v1)

            if color[v1] != 0 and color[v2] != 0:
                continue
            elif color[v1] != 0:
                visit(next_min_edge, v2)
            else:
                visit(next_min_edge, v1)

        return mst
