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
        relax_q: deque[int] = deque(maxlen=self.graph.num_vertices)
        relax_q_next_iter: deque[int] = deque(maxlen=self.graph.num_vertices)

        is_v_on_q = [False] * self.graph.num_vertices

        relax_q.append(0)
        is_v_on_q[0] = True
        self.edge_to[0] = None
        self.dist_to[0] = 0

        # +1 pass to make relax_q_next_iter work as a negative cycle identifier
        for _ in range(self.graph.num_vertices):
            while len(relax_q):
                next_v_to_relax = relax_q.popleft()
                # a vertex can't be on q on multiple instances
                is_v_on_q[next_v_to_relax] = False

                # parent checking heuristic
                if self.edge_to[next_v_to_relax]:
                    pred_v = self.edge_to[next_v_to_relax].other_vertex(  # type: ignore
                        next_v_to_relax)
                    if is_v_on_q[pred_v]:
                        # hold off relaxing this vertex, because predecessor will relax it again.
                        continue

                self._relax_vertex(
                    next_v_to_relax, is_v_on_q, relax_q_next_iter)

            relax_q, relax_q_next_iter = relax_q_next_iter, relax_q  # relax_q is empty now

        if len(relax_q):
            self.is_neg_cycle_reachable = True
        else:
            self.is_neg_cycle_reachable = False

    def _relax_vertex(self, v: int, is_v_on_q: list[bool], relax_q_next_iter: deque[int]):

        def relax(edge: WeightedEdge, to_v: int):
            new_dist = self.dist_to[v] + edge.weight

            if new_dist < self.dist_to[to_v]:
                self.dist_to[to_v] = new_dist
                self.edge_to[to_v] = edge
                if not is_v_on_q[to_v]:
                    relax_q_next_iter.append(to_v)
                    is_v_on_q[to_v] = True

        for adj_edge in self.graph.adj(v):
            to_v = adj_edge.other_vertex(v)
            relax(adj_edge, to_v)


if __name__ == "__main__":
    pass
