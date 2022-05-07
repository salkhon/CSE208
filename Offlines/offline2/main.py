from dsa1lib.graph import WeightedDirectedGraph, WeightedEdge
from shortestpath import BellmanFordSSSP, DijkstraSSSP, SingleSourceShortestPathAlgo


def run_SSSP(algo: SingleSourceShortestPathAlgo, destination: int):
    shortest_path = algo.shortest_path_to(destination)
    weight = sum(map(lambda edge: edge.weight, shortest_path))

    v_list = []
    v_list.append(destination)

    print("Shortest path cost:", weight)

    prev_v = destination
    for edge in shortest_path:
        v1 = edge.any_vertex()
        v2 = edge.other_vertex(v1)

        if v1 != prev_v:
            v_list.append(v1)
            prev_v = v1
        elif v2 != prev_v:
            v_list.append(v2)
            prev_v = v2
        else:
            raise RuntimeError("Shortest path is not consistent")

    v_list.reverse()
    print(" -> ".join([str(v) for v in v_list]))


if __name__ == "__main__":
    print("1. Dijkstra or 2. Bellman-Ford\t:", end="")
    opt = int(input())

    V, E = input().split()
    V, E = int(V), int(E)
    graph = WeightedDirectedGraph(V)

    for e in range(E):
        v1, v2, w = input().split()
        v1, v2, w = int(v1), int(v2), float(w)
        graph.add_edge(v1, v2, w)

    source, dest = input().split()
    source, dest = int(source), int(dest)

    if opt == 1:
        run_SSSP(DijkstraSSSP(graph, source), dest)
    else:
        bellmanford = BellmanFordSSSP(graph, source)
        if bellmanford.is_neg_cycle_reachable:
            print("The graph contains a negative cycle")
        else:
            print("The graph does not contain a negative cycle")
            run_SSSP(bellmanford, dest)
