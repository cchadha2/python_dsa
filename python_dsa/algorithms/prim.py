# Lazy version of Prim's algorithm.
import heapq
from collections import deque
from math import inf

from python_dsa.graph.edge_graph import Edge, EdgeWeightedGraph

from handy_decorators import timer


@timer
class PrimMST:

    def __init__(self, graph):
        self.marked = [False] * graph.num_vertices
        self.mst = deque()
        self.pq = []

        self.visit(graph, 0)
        # Quicker to just go through all of the vertices and adjacent edges rather than check if the
        # marked list is not all true in each iteration. This is O(n**2) in worst case. As opposed
        # to a O(logn) operation for each heappop in each iteration. Interesting that this is still
        # quicker despite many more iterations than doing the things the former way.
        # while not all(self.marked):
        while self.pq:
            edge = heapq.heappop(self.pq)
            vertex = edge.either()
            other_vertex = edge.other(vertex)

            if self.marked[vertex] and self.marked[other_vertex]:
                continue

            self.mst.append(edge)

            if not self.marked[vertex]:
                self.visit(graph, vertex)
            if not self.marked[other_vertex]:
                self.visit(graph, other_vertex)


    def visit(self, graph, vertex):
        self.marked[vertex] = True
        for edge in graph.adj[vertex]:
            if not self.marked[edge.other(vertex)]:
                heapq.heappush(self.pq, edge)

    def edges(self):
        return self.mst

    def weight(self):
        return sum(map(lambda edge: edge.weight, self.mst))


if __name__ == "__main__":
    graph = EdgeWeightedGraph(5)
    graph.add_edge(Edge(0, 1, 1.3))
    graph.add_edge(Edge(0, 2, 3.3))
    graph.add_edge(Edge(1, 4, 9.2))
    graph.add_edge(Edge(3, 1, 7.1))
    graph.add_edge(Edge(2, 3, 10.1))
    graph.add_edge(Edge(4, 0, 18.1))

    mst = PrimMST(graph)

    print(mst.edges())
    print(mst.weight())

