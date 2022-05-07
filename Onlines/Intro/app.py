from lib.dsa1lib.graph import DirectedGraph
from topologicalsort import TopologicalSort

if __name__ == "__main__":
    n = int(input())
    d = int(input())
    graph = DirectedGraph(n)
    for _ in range(d):
        s1, s2 = input().split()
        s1, s2 = int(s1) - 1, int(s2) - 1
        graph.add_edge(s1, s2)
    print(graph)
    topologicalsort = TopologicalSort(graph)

    if topologicalsort.order:
        for v in topologicalsort.order:
            print(v + 1)
    else:
        print("Not possible")
