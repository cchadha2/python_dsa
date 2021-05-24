# Depth-First-Order (graph traversal using DFS).
class DepthFirstOrder:

    def __init__(self, num_vertices, edges=()):
        # Override adj attribute with custom Vertex class.
        self.adj = [[] for _ in range(num_vertices)]
        self.num_vertices = num_vertices
        self.num_edges = 0
        for edge in edges:
            self._add_edge(edge)

        self._pre_order = []
        self._post_order = []
        self.visited = set()
        for vertex in range(self.num_vertices):
            self._dfs(vertex)

    def _add_edge(self, edge):
        from_vertex, to_vertex = edge
        self.adj[from_vertex].append(to_vertex)
        self.num_edges += 1

    def _dfs(self, source):
        if source not in self.visited:
            self.visited.add(source)
            self._pre_order.append(source)

            for adjacent_vertex in self.adj[source]:
                self._dfs(adjacent_vertex)

            self._post_order.append(source)

    def pre_order(self):
        return iter(self._pre_order)

    def post_order(self):
        return iter(self._post_order)

    def reverse_post_order(self):
        return reversed(self._post_order)

    def __str__(self):
        return str(self.adj)


if __name__ == "__main__":
    graph = DepthFirstOrder(7, edges=((0, 4), (2, 5), (2, 4), (2, 3), (3, 5), (4, 3), (4, 1), (5, 0), (1, 6), (1, 0)))
    print(graph)
    print(*graph.pre_order())
    print(*graph.post_order())

    # Example input from Algorithms book (pg. 579).
    graph = DepthFirstOrder(13, edges=((2, 0), (0, 5), (0, 1), (0, 6), (2, 3), (3, 5), (5, 4), (6, 4),
                                       (7, 6), (8, 7), (6, 9), (9, 11), (9, 10), (9, 12), (11, 12)))
    print(graph)
    print(*graph.pre_order())
    print(*graph.reverse_post_order())

    print(*graph.post_order())

