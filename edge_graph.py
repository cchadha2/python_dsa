# Edge weighted graph.
from dataclasses import dataclass


@dataclass
class Edge:
    vertex: int
    other_vertex: int
    weight: float

    def either(self):
        return self.vertex

    def other(self, given):
        if given == self.vertex:
            return self.other_vertex

        if given == self.other_vertex:
            return self.vertex

        raise ValueError("Given vertex is not part of edge")

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other parameter is not an edge")

        return self.weight < other.weight

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other parameter is not an edge")

        return self.weight > other.weight

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Other parameter is not an edge")

        return self.weight == other.weight


class EdgeWeightedGraph:

    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.num_edges = 0
        self.adj = [[] for _ in range(num_vertices)]

    def add_edge(self, edge):
        first = edge.either()
        second = edge.other(first)
        self.adj[first].append(edge)
        self.adj[second].append(edge)
        self.num_edges += 1

    def edges(self):
        all_edges = []
        for vertex, edges in enumerate(self.adj):
            for edge in edges:
                if edge.other(vertex) > vertex:
                    all_edges.append(edge)

        return all_edges

    def __str__(self):
        return str(self.adj)

if __name__ == "__main__":
    edge = Edge(0, 1, 0.4)
    other_edge = Edge(1, 2, 1.7)

    print(f"Is edge less than other edge? {edge < other_edge}")
    print(f"Is edge greater than other edge? {edge > other_edge}")
    print(f"Is edge equal to the other edge? {edge == other_edge}")

    graph = EdgeWeightedGraph(5)
    graph.add_edge(edge)
    graph.add_edge(other_edge)
    graph.add_edge(Edge(1, 3, 2.4))
    graph.add_edge(Edge(0, 4, 1.5))

    print(graph)
    print(graph.edges())

