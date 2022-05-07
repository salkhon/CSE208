class Graph:
    """Abstract class for Graph. 
    """

    def __init__(self, V: int) -> None:
        self._adj = [[] for _ in range(V)]
        self._V = V
        self._E = 0

    @property
    def num_vertices(self) -> int:
        """Number of vertices in the undirected graph. 

        Returns:
            int: Number of vertices in the graph. 
        """
        return self._V

    @property
    def num_edges(self) -> int:
        """Number of edges in the undirected graph. 

        Returns:
            int: Number of edges in the graph. 
        """
        return self._E
    
    def adj(self, v: int) -> list[int]:
        """The adjacent vertices of v. 

        Args:
            v (int): Vertex whose neighbors to find. 

        Returns:
            list[int]: Adjacent vertices to the provided vertex. 
        """
        if v < 0 or v > self.num_vertices:
            raise ValueError(
                "Vertex in not within bounds of the number of vertex for the graph.")
        return self._adj[v]

    def add_edge(self, v1: int, v2: int) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        repre = ""
        for v in range(self._V):
            repre += f"{v}: " + str(self._adj[v]) + "\n"
        return repre



class UndirectedGraph(Graph):
    """Implementation of an undirected graph.
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, v1: int, v2: int) -> None:
        """Adds an undirected edge between v1 and v2.

        Args:
            v1 (int): Vertex 1. 
            v2 (int): Vertex 2. 
        """
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError(
                "Vertex in not within bounds of the number of vertex for the graph.")
        self._adj[v1].append(v2)
        self._adj[v2].append(v1)

        self._E += 1


class DirectedGraph(Graph):
    """Implementation of a directed graph
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, v1: int, v2: int) -> None:
        """Adds a directed edge between v1 and v2.

        Args:
            v1 (int): Source vertex. 
            v2 (int): Target vertex. 
        """
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError(
                "Vertex in not within bounds of the number of vertex for the graph.")

        self._adj[v1].append(v2)
        self._E += 1


class WeightedEdge:
    """Implementation for weighted edge, to be used with WeightedGraph or WeightedUndirectedGraph. 
    """

    def __init__(self, v1: int, v2: int, weight: float, is_directed: bool) -> None:
        self._v1 = v1
        self._v2 = v2
        self._weight = weight
        self.is_directed = is_directed

    @property
    def weight(self) -> float:
        """Weight of the edge. 

        Returns:
            float: Returns the weight of the edge. 
        """
        return self._weight

    @property
    def v1(self) -> int:
        """Returns one vertex 

        Returns:
            float: Returns one vertex.  
        """
        return self._v1

    def another_vertex(self, v: int) -> int:
        """Another vertex.  

        Args:
            v (int): One vertex.  

        Returns:
            float: Returns the other vertex of the provided one. 
        """
        if v != self._v1 and v != self._v2:
            raise ValueError("Provided vertex is not on this edge.")
        return self._v1 if v != self._v1 else self._v2

    @property
    def edge_from(self):
        if not self.is_directed:
            return AttributeError("Undirected edge does not have from vertex")
        return self._v1

    @property
    def edge_to(self):
        if not self.is_directed:
            return AttributeError("Undirected edge does not have to vertex")
        return self._v2

    def __repr__(self):
        return f"({self._v1}, {self._v2})"


class WeightedGraph(Graph):
    def __init__(self, V: int) -> None:
        super().__init__(V)

    def adj(self, v: int) -> list[WeightedEdge]:
        if v < 0 or v > self.num_vertices:
            raise ValueError(
                "Vertex in not within bounds of the number of vertex for the graph.")
        return self._adj[v]


class WeightedUndirectedGraph(WeightedGraph):
    """Implementation for weighted undirected graph.
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, edge: WeightedEdge) -> None:
        v1 = edge.v1
        v2 = edge.another_vertex(v1)
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError("Edge has vertices outside of range.")
        self._adj[v1].append(edge)
        self._adj[v2].append(edge)


class WeightedDirectedGraph(Graph):
    """Implementation for weighted directed graph
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, edge: WeightedEdge) -> None:
        v1 = edge.v1
        v2 = edge.another_vertex(v1)
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError("Edge has vertices outside of range.")
        self._adj[v1].append(edge)
