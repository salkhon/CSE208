from typing import cast
from graph import Graph, DirectedGraph
from collections import deque


class TraversalAlgo:
    def __init__(self, graph: Graph, source: int):
        self._graph = graph
        self._source = source
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

    def __init__(self, graph: Graph, source: int):
        super().__init__(graph, source)
        self._cycle_exists = False
        self._traverse()

    def _traverse(self):
        def visit(v: int):
            self._color[v] = 1
            for neighbor in self._graph.adj(v):
                if self._color[neighbor] == 0:
                    self._parent[neighbor] = v
                    visit(neighbor)
                elif self._color[neighbor] == 1:
                    self._cycle_exists = True
            self._color[v] = 2

        visit(self._source)

    @property
    def has_cycle(self):
        return self._cycle_exists


class BFS(TraversalAlgo):
    """Traverses Unweighted graph."""

    def __init__(self, graph: Graph, source: int):
        super().__init__(graph, source)
        self._traverse()

    def _traverse(self):
        q = deque(maxlen=self._graph.num_vertices)

        def visit(v: int):
            for neighbor in self._graph.adj(v):
                if self._color[neighbor] == 0:
                    self._color[neighbor] = 1
                    self._parent[neighbor] = v
                    q.append(neighbor)
            self._color[v] = 2

        self._parent[self._source] = -1
        self._color[self._source] = 1
        q.append(self._source)

        while len(q):
            v = q.popleft()
            visit(v)


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
