from collections import deque
from typing import List, Tuple
from dsa1lib.graph import *
import abc


class FlowEdge(WeightedDirectedEdge):
    def __init__(self, edge: WeightedEdge):
        super().__init__(edge.any_vertex(), edge.other_vertex(edge.any_vertex()), edge.weight)
        self.flow = 0

    @property
    def capacity(self) -> int:
        return int(self.weight)

    def residual_capacity(self, from_v: int) -> int:
        if self.capacity < 0:
            # convention: negative capacity edges can't carry flow
            return 0
        elif from_v == self._v1:
            return self.capacity - self.flow
        elif from_v == self._v2:
            return self.flow
        else:
            raise ValueError("vertex does not belong to flow edge")

    def push_flow(self, aug_flow: int, from_v: int):
        if from_v == self._v1:
            self.flow += aug_flow
        elif from_v == self._v2:
            self.flow -= aug_flow
        else:
            raise ValueError("vertex does not belong to flow edge")


class FlowNetwork(WeightedDirectedGraph):
    def __init__(self, graph: WeightedDirectedGraph, s: int, t: int):
        super().__init__(graph.num_vertices)
        self.s = s
        self.t = t
        self._incoming_edges = [[] for v in range(graph.num_vertices)]
        for v1 in range(graph.num_vertices):
            for edge in graph.adj(v1):
                flow_edge = FlowEdge(edge)
                self._adj[v1].append(flow_edge)

                v2 = edge.other_vertex(v1)
                self._incoming_edges[v2].append(flow_edge)

    def incoming_edges(self, v: int) -> List[FlowEdge]:
        return self._incoming_edges[v]

    def outgoing_edges(self, v: int) -> List[FlowEdge]:
        return self._adj[v]

    @property
    def flow(self) -> int:
        flow = 0
        for edge in self.outgoing_edges(self.s):
            flow += edge.flow
        return flow

    def __repr__(self) -> str:
        rep = ""
        for v in range(self.num_vertices):
            rep += f"Vertex {v}: \n"
            for edge in self.outgoing_edges(v):
                rep += f"\t{edge} {edge.flow} / {edge.capacity}\n"
            rep += "\n"
        return rep


class FordFulkersonMethod(abc.ABC):
    def __init__(self, graph: WeightedDirectedGraph, s: int, t: int):
        """Finds max flow, min cut on a flow network. 

        Args:
            graph (WeightedDirectedGraph): Flow network graph
            s (int): Vertex that is the source. SOURCE CAN'T HAVE INCOMING EDGES.
            t (int): Vertex that is the target. TARGET CAN'T HAVE OUTGOING EDGES.
        """

        self.flow_network = FlowNetwork(graph, s, t)
        self.s = s
        self.t = t
        self.maxflow = 0
        self.mincut = []

    @abc.abstractmethod
    def find_augmenting_path(self) -> Tuple[int, List[FlowEdge]]:
        """Finds augmenting path and minimum residual capacity on that path in the residual network.

        Returns:
            Tuple[int, List[WeightedDirectedEdge]]: minimum residual capacity on the augmenting path, the augmenting path
        """
        pass

    @abc.abstractmethod
    def compute_mincut(self) -> List[int]:
        """Stores mincut after no augmenting path is found in Ford-Fulkerson method. Returns the vertices stored in 
        the s-cut. 
        """
        pass

    def _push_flow_through_aug_path(self, min_residual_cap: int, aug_path: List[FlowEdge]):
        from_v = self.s
        for edge in aug_path:
            edge.push_flow(min_residual_cap, from_v)
            from_v = edge.other_vertex(from_v)

    def _run_maxflow_mincut(self) -> None:
        """Ford-Fulkerson method of finding max flow. Implement find_augmenting_path() before calling this. 
        """

        is_there_aug_path = True

        while is_there_aug_path:
            min_residual_cap, aug_path = self.find_augmenting_path()

            if not aug_path:
                is_there_aug_path = False
            else:
                self._push_flow_through_aug_path(min_residual_cap, aug_path)

        self.maxflow = self.flow_network.flow
        self.mincut = self.compute_mincut()


class EdmondsKarp(FordFulkersonMethod):
    def __init__(self, graph: WeightedDirectedGraph, s: int, t: int):
        super().__init__(graph, s, t)

        self.q = deque(maxlen=self.flow_network.num_vertices)
        self.color = [0] * self.flow_network.num_vertices
        self.residual_edge_to: List = [
            None] * self.flow_network.num_vertices

        self._run_maxflow_mincut()

    def find_augmenting_path(self) -> Tuple[int, List[FlowEdge]]:
        """Uses BFS on residual network, choosing edges that have residual capacity left. When no augmenting path is available, 
        it stores the mincut s-side vertices, and returns (-1, []).

        Returns:
            Tuple[int, List[FlowEdge]]: Tuple containing augmenting path, and the minimum capacity on that augmenting path.
        """

        self.q.clear()
        for v in range(self.flow_network.num_vertices):
            self.color[v] = 0
            self.residual_edge_to[v] = None

        self.q.append(self.s)
        self.color[self.s] = 1

        while self.q:
            v1 = self.q.popleft()
            self.color[v1] = 2

            for edge in self.flow_network.outgoing_edges(v1):
                v2 = edge.other_vertex(v1)

                if edge.residual_capacity(v1) and self.color[v2] == 0:
                    self.color[v2] = 1
                    self.residual_edge_to[v2] = edge
                    if v2 == self.t:
                        return self._construct_aug_path()
                    self.q.append(v2)

            for edge in self.flow_network.incoming_edges(v1):
                v2 = edge.other_vertex(v1)

                if edge.residual_capacity(v1) and self.color[v2] == 0:
                    self.color[v2] = 1
                    self.residual_edge_to[v2] = edge
                    self.q.append(v2)

        if self.residual_edge_to[self.t]:
            return self._construct_aug_path()
        else:
            return (-1, [])  # not aug path

    def compute_mincut(self) -> List[int]:
        mincut = [self.s]
        for v in range(self.flow_network.num_vertices):
            if self.residual_edge_to[v]:
                mincut.append(v)
        return mincut

    def _construct_aug_path(self) -> Tuple[int, List[FlowEdge]]:
        aug_path: List[FlowEdge] = []
        min_cap = float("inf")
        v = self.t
        while v != self.s:
            edge_to = self.residual_edge_to[v]
            assert edge_to is not None

            aug_path.append(edge_to)
            v = edge_to.other_vertex(v)
            min_cap = min(min_cap, edge_to.residual_capacity(v))

        aug_path.reverse()

        return int(min_cap), aug_path


if __name__ == "__main__":
    for i in range(1, 8):
        print("--------------------", i, "----------------------------------")
        with open(f"testcases/in{i}.txt", "r") as file:
            lines = file.readlines()

        V, E = lines[0].split()
        V, E = int(V), int(E)

        graph = WeightedDirectedGraph(V)

        for e in range(E):
            v1, v2, w = lines[1 + e].split()
            v1, v2, w = int(v1), int(v2), int(w)
            graph.add_edge(v1, v2, w)

        s, t = lines[len(lines) - 1].split()
        s, t = int(s), int(t)

        edmondskarp = EdmondsKarp(graph, s, t)
        print(edmondskarp.maxflow)
        print(edmondskarp.flow_network)
        print(edmondskarp.mincut)
        print("--------------------", i,
              "----------------------------------\n\n")
