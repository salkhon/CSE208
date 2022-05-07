from typing import Union
from lib.dsa1lib.graph import DirectedGraph

class TopologicalSort:
    def __init__(self, graph: DirectedGraph):
        self.graph = graph
        self.is_marked = [False for _ in range(graph.num_vertices)]
        self.order = self._top_sort()
        if self.order:
            self.order.reverse()

    def _top_sort(self) -> Union[list[int], None]:
        order: Union[list[int], None] = []
        on_stack: list[bool] = [False for _ in range(self.graph.num_vertices)]
        no_cycle = True
        for v in range(self.graph.num_vertices):
            if not self.is_marked[v]:
                self.is_marked[v] = True
                on_stack[v] = True
                no_cycle = self._dfs(v, order, on_stack)
                on_stack[v] = False
                order.append(v)
                print("appending:", v)
            if not no_cycle:
                order = None
                break
        
        return order

    def _dfs(self, v: int, order: list[int], on_stack: list[bool]) -> bool:
        print("visiting", v)
        no_cycle = True
        for neighbor in self.graph.adj(v):
            if not self.is_marked[neighbor]:
                self.is_marked[neighbor] = True
                on_stack[neighbor] = True
                no_cycle = self._dfs(neighbor, order, on_stack)
                on_stack[neighbor] = False
                order.append(neighbor)
                print("appending:-", v)
            elif on_stack[neighbor]:
                no_cycle = False

            if not no_cycle:
                break
        
        return no_cycle

        