from maxflowmincut import *


if __name__ == "__main__":
    m, n = input().split()
    m, n = int(m), int(n)
    xlen, ylen = input().split()
    xlen, ylen = int(xlen), int(ylen)
    p = int(input())

    num_vertices = 2 + xlen + ylen
    s, t = 0, 1
    graph = WeightedDirectedGraph(num_vertices)

    def boy_idx(i: int) -> int:
        return 2 + i

    def girl_idx(i: int) -> int:
        return 2 + xlen + i

    for i in range(xlen):
        graph.add_edge(s, boy_idx(i), n)

    for i in range(ylen):
        graph.add_edge(girl_idx(i), t, n)

    for i in range(p):
        x, y = input().split()
        x, y = int(x), int(y)
        graph.add_edge(boy_idx(x), girl_idx(y), m)

    edmondskarp = EdmondsKarp(graph, s, t)
    print(edmondskarp.maxflow)
    flownetwork = edmondskarp.flow_network

    flow_mat = [[0 for _ in range(ylen)] for _ in range(xlen)]

    for x in range(xlen):
        for edge in flownetwork.outgoing_edges(boy_idx(x)):
            y = edge.other_vertex(boy_idx(x)) - 2 - xlen
            flow_mat[x][y] = edge.flow

    for x in range(xlen):
        for y in range(ylen):
            print(f"({x}, {y}) {flow_mat[x][y]}")
