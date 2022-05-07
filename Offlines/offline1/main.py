from dsa1lib.graph import WeightedUndirectedGraph, WeightedEdge
from mst import KruskalMST, PrimMST

if __name__ == "__main__":
    V, E = [int(inp) for inp in input().split()]
    graph = WeightedUndirectedGraph(V)

    for edge in range(E):
        v1, v2, w = input().split()
        graph.add_edge(int(v1), int(v2), float(w))

    kruskal = KruskalMST(graph)
    prim = PrimMST(graph)

    print("Cost of the minimum spanning tree :", prim.mst_weight)

    prim_edges = [(edge.any_vertex(), edge.other_vertex(
        edge.any_vertex())) for edge in prim.mst]
    kruskal_edges = [(edge.any_vertex(), edge.other_vertex(
        edge.any_vertex())) for edge in kruskal.mst]

    print("List of edges selected by Prim's:", prim_edges)
    print("List of edges selected by Kruskal's:", kruskal_edges)
