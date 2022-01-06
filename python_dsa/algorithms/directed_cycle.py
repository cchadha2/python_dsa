# Find a cycle in a directed graph.
from python_dsa.graph.directed_graph_recursive import DiGraphRecursive


class DirectedCycle(DiGraphRecursive):

    def __init__(self, num_vertices, edges=()):
        super().__init__(num_vertices, edges)

        self.on_stack = [False] * num_vertices
        self.edge_to = [None] * num_vertices
        self.cycle = []

        for vertex in range(num_vertices):
            self.dfs(vertex)

    def dfs(self, source):
        if not self.visited[source]:
            self.visited[source] = True
            self.on_stack[source] = True

            for adjacent_vertex in self.adj[source]:
                if self.has_cycle():
                    return
                elif not self.visited[adjacent_vertex]:
                    self.edge_to[adjacent_vertex] = source
                    self.dfs(adjacent_vertex)
                elif self.on_stack[adjacent_vertex]:
                    self.cycle.clear()
                    vertex = source
                    while vertex != adjacent_vertex:
                        self.cycle.append(vertex)
                        vertex = self.edge_to[vertex]

                    self.cycle.append(adjacent_vertex)
                    self.cycle.append(source)

            self.on_stack[source] = False

    def has_cycle(self):
        return bool(self.cycle)

    def __iter__(self):
        return reversed(self.cycle)


if __name__ == "__main__":
    graph = DirectedCycle(7, edges=((0, 4), (2, 5), (2, 4), (2, 3), (3, 5), (4, 3), (4, 1), (5, 0), (1, 6), (1, 0)))
    print(graph)
    print(graph.has_cycle())
    print(*graph)

    # Example input from Algorithms book (pg. 579).
    graph = DirectedCycle(13, edges=((2, 0), (0, 5), (0, 1), (0, 6), (2, 3), (3, 5), (5, 4), (6, 4),
                                     (7, 6), (8, 7), (6, 9), (9, 11), (9, 10), (9, 12), (11, 12)))
    print(graph)
    print(graph.has_cycle())
    print(*graph)


