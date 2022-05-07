from graph import Graph
from collections import deque

class TraversalAlgo:
    def __init__(self, graph: Graph, source: int):
        self.graph = graph
        self.source = source
        self.parent = [0] * self.graph.num_vertices
        self.color = [0] * self.graph.num_vertices

    def traverse(self):
        return NotImplementedError


class DFS(TraversalAlgo):
    def __init__(self, graph: Graph, source: int):
        super().__init__(graph, source)
        self.cycle_exists = False

    def traverse(self):
        def visit(v: int):
            self.color[v] = 1
            for neighbor in self.graph.adj(v):
                if self.color[neighbor] == 0:
                    self.parent[neighbor] = v
                    visit(neighbor)
                elif self.color[neighbor] == 1:
                    self.cycle_exists = True
            self.color[v] = 2
        visit(self.source)


class BFS(TraversalAlgo):
    def __init__(self, graph: Graph, source: int):
        super().__init__(graph, source)

    def traverse(self):
        q = deque(maxlen=self.graph.num_vertices)

        def visit(v: int):
            for neighbor in self.graph.adj(v):
                if self.color[neighbor] == 0:
                    self.color[neighbor] = 1
                    self.parent[neighbor] = v
                    q.append(neighbor)
            self.color[v] = 2

        self.color[self.source] = 1
        q.append(self.source)

        while len(q):
            v = q.popleft()
            visit(v)


if __name__ == "__main__":
    pass
