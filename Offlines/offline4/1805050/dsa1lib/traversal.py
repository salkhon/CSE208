from typing import cast
from graph import Graph, DirectedGraph
from collections import deque


class TraversalAlgo:
    def __init__(self, graph: Graph):
        self._graph = graph
        self._parent = [0] * self._graph.num_vertices
        self._color = [0] * self._graph.num_vertices

    def _traverse(self):
        return NotImplementedError

    def path_to(self, v: int) -> list[int]:
        path = [v]
        p = v
        while p != -1:
            p = self._parent[p]
            path.append(p)
        return path

    def is_reachable(self, v: int) -> bool:
        return self._color[v] != 0


class DFS(TraversalAlgo):
    """Traverses Unweighted graph."""

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self._cycle_exists = False
        self._traverse()

    def _visit(self, v: int):
        self._color[v] = 1
        for neighbor in self._graph.adj(v):
            if self._color[neighbor] == 0:
                self._parent[neighbor] = v
                self._visit(neighbor)
            elif self._color[neighbor] == 1:
                self._cycle_exists = True
        self._color[v] = 2

    def _traverse(self):
        for v in range(self._graph.num_vertices):
            self._visit(v)

    @property
    def has_cycle(self):
        return self._cycle_exists

    def is_connected(self) -> bool:
        return all(self._color)


class BFS(TraversalAlgo):
    """Traverses Unweighted graph."""

    def __init__(self, graph: Graph, source: int):
        super().__init__(graph)
        self.source = source
        self._traverse()

    def _visit(self, v: int, q: deque[int]):
        for neighbor in self._graph.adj(v):
            if self._color[neighbor] == 0:
                self._color[neighbor] = 1
                self._parent[neighbor] = v
                q.append(neighbor)
        self._color[v] = 2

    def _traverse(self):
        q = deque(maxlen=self._graph.num_vertices)

        self._parent[self.source] = -1
        self._color[self.source] = 1
        q.append(self.source)

        while len(q):
            v = q.popleft()
            self._visit(v, q)


if __name__ == "__main__":
    dg = DirectedGraph(5)
    dg.add_edge(0, 1)
    dg.add_edge(0, 2)
    dg.add_edge(0, 3)
    dg.add_edge(1, 2)
    dg.add_edge(2, 4)
    dg.add_edge(3, 3)
    dg.add_edge(4, 4)
    bfs = BFS(dg, 0)
