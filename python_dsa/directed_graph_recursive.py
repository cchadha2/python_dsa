# Directed graph (recursive).
class DiGraph:

    def __init__(self, num_vertices, edges=()):
        self.adj = [[] for _ in range(num_vertices)]
        self.num_vertices = num_vertices
        self.num_edges = 0
        for edge in edges:
            self._add_edge(edge)

        self.visited = [False] * num_vertices

    def _add_edge(self, edge):
        from_vertex, to_vertex = edge
        self.adj[from_vertex].append(to_vertex)
        self.num_edges += 1

    def dfs(self, source):
        if not self.visited[source]:
            self.visited[source] = True

            for adjacent_vertex in self.adj[source]:
                self.dfs(adjacent_vertex)

    def __str__(self):
        return str(self.adj)


if __name__ == "__main__":
    graph = DiGraph(7, edges=((0, 4), (2, 5), (2, 4), (2, 3), (3, 5), (4, 3), (4, 1), (5, 0), (1, 6), (1, 0)))
    print(graph)
    print(graph.dfs(0))
    print(graph.visited)

    # Example input from Algorithms book (pg. 579).
    graph = DiGraph(13, edges=((2, 0), (0, 5), (0, 1), (0, 6), (2, 3), (3, 5), (5, 4), (6, 4),
                               (7, 6), (8, 7), (6, 9), (9, 11), (9, 10), (9, 12), (11, 12)))
    print(graph)
    print(graph.dfs(0))
    print(graph.visited)

