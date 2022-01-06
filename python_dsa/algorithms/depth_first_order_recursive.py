# Depth-First-Order (graph traversal using DFS).
from python_dsa.graph.directed_graph_recursive import DiGraphRecursive


class DepthFirstOrder(DiGraphRecursive):

    def __init__(self, num_vertices, edges=()):
        super().__init__(num_vertices, edges)

        self._pre_order = []
        self._post_order = []
        for vertex in range(num_vertices):
            self.dfs(vertex)

    def dfs(self, source):
        if not self.visited[source]:
            self.visited[source] = True
            self._pre_order.append(source)

            for adjacent_vertex in self.adj[source]:
                self.dfs(adjacent_vertex)

            self._post_order.append(source)

    def pre_order(self):
        return iter(self._pre_order)

    def post_order(self):
        return iter(self._post_order)

    def reverse_post_order(self):
        return reversed(self._post_order)


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

