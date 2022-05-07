from collections import deque
from dsa1lib.graph import WeightedEdge, WeightedGraph
from dsa1lib.indexheap import IndexedMinPQ
import math
import abc


class SingleSourceShortestPathAlgo(abc.ABC):

    def __init__(self, graph: WeightedGraph, source: int):
        self.graph = graph
        self.source = source
        self.edge_to: list[WeightedEdge | None] = [
            None] * self.graph.num_vertices
        self.dist_to = [math.inf] * self.graph.num_vertices
        self._find_shortest_path()

    @abc.abstractmethod
    def _find_shortest_path(self):
        raise NotImplementedError()

    def shortest_path_to(self, v: int) -> list[WeightedEdge]:
        shortest_path = []
        u = v
        while self.edge_to[u]:
            shortest_path.append(self.edge_to[u])
            u = self.edge_to[u].other_vertex(u)  # type: ignore
        return shortest_path

    @property
    def shortest_path_tree(self) -> list[WeightedEdge]:
        spt = []
        for v in range(self.graph.num_vertices):
            if self.edge_to[v]:
                spt.append(self.edge_to[v])
        return spt

    @property
    def shortest_path_tree_cost(self) -> float:
        return sum(map(lambda edge: edge.weight, self.shortest_path_tree))


class DijkstraSSSP(SingleSourceShortestPathAlgo):

    def __init__(self, graph: WeightedGraph, source: int):
        super().__init__(graph, source)

    def _find_shortest_path(self):
        index_min_pq = IndexedMinPQ(self.graph.num_vertices)

        self.dist_to[self.source] = 0.0
        self.edge_to[self.source] = None
        index_min_pq.insert(self.source, 0.0)

        while len(index_min_pq):
            closest_vertex, _ = index_min_pq.del_min()
            self._relax_vertex(closest_vertex, index_min_pq)

    def _relax_vertex(self, vertex: int, index_min_pq: IndexedMinPQ):
        """Relaxes adj edges of the vertex

        Args:
            vertex (int): Vertex whose adj edges to relax
            index_min_pq (IndexedMinPQ): PQ holding shortest path order. 
        """

        def relax(edge: WeightedEdge, to_vertex: int):
            pred = edge.other_vertex(to_vertex)
            new_dist = self.dist_to[pred] + edge.weight

            if new_dist < self.dist_to[to_vertex]:
                self.edge_to[to_vertex] = edge
                self.dist_to[to_vertex] = new_dist

                if index_min_pq.key_of_index(to_vertex) is None:
                    index_min_pq.insert(to_vertex, new_dist)
                else:
                    index_min_pq.decrease_key(to_vertex, new_dist)

        for adj_edge in self.graph.adj(vertex):
            to_vertex = adj_edge.other_vertex(vertex)
            relax(adj_edge, to_vertex)


class BellmanFordSSSP(SingleSourceShortestPathAlgo):

    def __init__(self, graph: WeightedGraph, source: int):
        super().__init__(graph, source)

    def shortest_path_to(self, v: int) -> list[WeightedEdge] | None:
        if self.is_neg_cycle_reachable:
            return None
        return super().shortest_path_to(v)

    def shortest_path_tree(self) -> list[WeightedEdge] | None:
        if self.is_neg_cycle_reachable:
            return None
        return super().shortest_path_tree

    def _find_shortest_path(self):
        self.dist_to[self.source] = 0
        self.edge_to[self.source] = None

        for _ in range(self.graph.num_vertices - 1):
            for edge in self.graph.get_all_edges():
                # implicitly assuming directed edge from v1 to v2 of the edge
                self._relax_edge(edge, edge.any_vertex(),
                                 edge.other_vertex(edge.any_vertex()))

        self.is_neg_cycle_reachable = self._any_relaxable_edge()

    def _relax_edge(self, edge: WeightedEdge, from_v: int, to_v: int):
        dist_by_this_edge = self.dist_to[from_v] + edge.weight

        if dist_by_this_edge < self.dist_to[to_v]:
            self.dist_to[to_v] = dist_by_this_edge
            self.edge_to[to_v] = edge

    def _any_relaxable_edge(self) -> bool:
        for edge in self.graph.get_all_edges():
            from_v = edge.any_vertex()
            to_v = edge.other_vertex(from_v)
            dist_by_this_edge = self.dist_to[from_v] + edge.weight

            if dist_by_this_edge < self.dist_to[to_v]:
                return True
        else:
            return False


if __name__ == "__main__":
    pass
