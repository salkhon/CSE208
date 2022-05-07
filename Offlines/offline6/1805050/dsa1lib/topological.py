from typing import cast
from graph import DirectedGraph
from traversal import DFS


class TopologicalSort:
    def __init__(self, graph: DirectedGraph):
        self.graph = graph
        dfs = DFS(graph)
        self._order = None
        if not dfs.has_cycle:
            self._order = PostOrder(self.graph).order
            self._order.reverse()

    @property
    def order(self):
        return self._order


class PostOrder:
    def __init__(self, graph: DirectedGraph):
        self.graph = graph
        self.color = [0] * self.graph.num_vertices
        self._order = self._get_order()

    def _get_order(self) -> list[int]:
        order = []

        def _dfs(v: int):
            self.color[v] = 1
            for neighbor in self.graph.adj(v):
                if self.color[neighbor] == 0:
                    _dfs(neighbor)
            order.append(v)
            self.color[v] = 2

        for v in range(self.graph.num_vertices):
            if self.color[v] == 0:
                _dfs(v)

        return order

    @property
    def order(self) -> list[int]:
        return self._order


if __name__ == "__main__":
    v, e = input().split()
    v, e = int(v), int(e)
    graph = DirectedGraph(v)
    for edge in range(e):
        v1, v2 = input().split()
        v1, v2 = int(v1) - 1, int(v2) - 1
        graph.add_edge(v1, v2)

    print(TopologicalSort(graph).order)
