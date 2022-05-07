from typing import List, Union, cast
import abc

class WeightedEdge(abc.ABC):
    """Implementation for weighted edge, to be used with WeightedGraph or WeightedUndirectedGraph. 
    """

    def __init__(self, v1: int, v2: int, weight: float) -> None:
        self._v1 = v1
        self._v2 = v2
        self._weight = weight

    def any_vertex(self) -> int:
        """First vertex

        Returns:
            int: First vertex
        """        
        return self._v1

    def other_vertex(self, v: int) -> int:
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
    def weight(self) -> float:
        """Weight of the edge. 

        Returns:
            float: Returns the weight of the edge. 
        """
        return self._weight

    @weight.setter
    def weight(self, value: float):
        self._weight = value

    def __repr__(self):
        return f"({self._v1}, {self._v2})"

    def __lt__(self, other: "WeightedEdge") -> bool:
        """Less than if the weights are less than the other edge. (For sorting wrt to the edge weight)

        Args:
            other (WeightedEdge): The other weighted edge. 

        Returns:
            bool: True iff the weight is less. 
        """
        return self._weight < other._weight


class WeightedUndirectedEdge(WeightedEdge):
    def __init__(self, v1: int, v2: int, weight):
        super().__init__(v1, v2, weight)

    def __eq__(self, other: "WeightedEdge") -> bool:
        """Equal if the pair of vertices and weights match. 

        Args:
            other (WeightedEdge): The other weighted edge. 

        Returns:
            bool: True iff pair of vertices match, and weights are equal. 
        """
        return (self.weight, self._v1, self._v2) == (other.weight, other._v1, other._v2) or \
            (self.weight, self._v1, self._v2) == (
                other.weight, other._v2, other._v1)

    def __hash__(self):
        """Hash depends on the pair of vertices (order not considered), and weight

        Returns:
            int: hashed value. 
        """
        return hash((self.weight, self._v1, self._v2)) \
            if self._v1 < self._v2 else hash((self.weight, self._v2, self._v1))


class WeightedDirectedEdge(WeightedEdge):
    def __init__(self, v1: int, v2: int, weight):
        super().__init__(v1, v2, weight)

    @property
    def edge_from(self):
        return self._v1

    @property
    def edge_to(self):
        return self._v2

    def __eq__(self, other: "WeightedEdge") -> bool:
        """Equal if the pair of vertices (in order) and weights match. 

        Args:
            other (WeightedEdge): The other weighted edge. 

        Returns:
            bool: True iff pair of from and to vertices, and weights are equal. 
        """
        return (self.weight, self._v1, self._v2) == (other.weight, other._v1, other._v2) or \
            (self.weight, self._v1, self._v2) == (
                other.weight, other._v2, other._v1)

    def __hash__(self):
        """Hash depends on the pair of vertices (order is considered), and weight

        Returns:
            int: hashed value. 
        """
        return hash((self.weight, self._v1, self._v2))


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

    def adj(self, v: int) -> List[int]:
        """The adjacent vertices of v. This impl is for un-weighted graphs. 

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

    def reverse(self) -> "DirectedGraph":
        graph = DirectedGraph(self.num_vertices)
        for v1 in range(self.num_vertices):
            for v2 in cast(List[int], self.adj(v1)):
                graph.add_edge(v2, v1)
        return graph


class WeightedGraph(Graph):
    def __init__(self, V: int) -> None:
        super().__init__(V)

    def adj(self, v: int) -> List[WeightedEdge]:
        if v < 0 or v > self.num_vertices:
            raise ValueError(
                "Vertex in not within bounds of the number of vertex for the graph.")
        return self._adj[v]

    def get_all_edges(self) -> List[WeightedEdge]:
        edgeset = set()
        for v in range(self.num_vertices):
            for neib in self.adj(v):
                edgeset.add(neib)

        return list(edgeset)


class WeightedUndirectedGraph(WeightedGraph):
    """Implementation for weighted undirected graph.
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, v1: int, v2: int, weight: float):
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError("Edge has vertices outside of range.")

        edge = WeightedUndirectedEdge(v1, v2, weight)
        self._adj[v1].append(edge)
        self._adj[v2].append(edge)


class WeightedDirectedGraph(WeightedGraph):
    """Implementation for weighted directed graph
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)

    def add_edge(self, v1: int, v2: int, weight: float):
        if v1 < 0 or v2 < 0 or v1 > self.num_vertices or v2 > self.num_vertices:
            raise ValueError("Edge has vertices outside of range.")

        edge = WeightedDirectedEdge(v1, v2, weight)
        self._adj[v1].append(edge)
