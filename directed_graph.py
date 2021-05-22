# Directed graph.
from undirected_graph import Graph


class DiGraph(Graph):

    def add_edge(self, edge):
        """Same as Graph but only add edge in a single direction."""
        from_vertex, to_vertex = edge
        self.adj[from_vertex].add(to_vertex)
        self.num_edges += 1

    def reverse(self):
        """Returns a new DiGraph with directions reversed."""
        reverse_digraph = DiGraph(self.num_vertices)
        for vertex, edges in enumerate(self.adj):
            for to_vertex in edges:
                reverse_digraph.add_edge((to_vertex, vertex))

        return reverse_digraph

if __name__ == "__main__":
    graph = DiGraph(6, edges=((2, 4), (2, 3), (2, 5), (4, 1), (1, 0), (5, 0), (4, 3)))
    print(graph)

    print(graph.num_edges)
    print(graph.num_vertices)

    graph.add_edge((0, 2))
    print(graph)
    print(graph.num_edges)

    graph.add_vertex()
    graph.add_edge((1, 6))
    print(*graph.dfs(2))
    print(*graph.bfs(2))

    print(graph)
    print(graph.reverse())

