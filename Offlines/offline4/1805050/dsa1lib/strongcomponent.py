from topological import PostOrder
from graph import DirectedGraph


class KosarajuStringComponent:
    def __init__(self, dg: DirectedGraph):
        self._dg = dg
        self.component_ids = [i for i in range(dg.num_vertices)]
        rev_post_order = PostOrder(self._dg.reverse()).order
        self.num_components = self._mark_components(rev_post_order)

    def _mark_components(self, rev_post_order: list[int]):
        color = [0] * self._dg.num_vertices

        def visit(v: int, id: int):
            self.component_ids[v] = id
            color[v] = 1
            for neighbor in self._dg.adj(v):
                if color[neighbor] == 0:
                    visit(neighbor, id)

        id = 0
        for v in rev_post_order:
            if color[0] == 0:
                visit(v, id)
                id += 1

        return id

    def is_same_component(self, v1: int, v2: int) -> bool:
        return self.component_ids[v1] == self.component_ids[v2]

    def component_members(self, v: int) -> list[int]:
        return [u for u in range(self._dg.num_vertices) if self.component_ids[u] == self.component_ids[v]]
