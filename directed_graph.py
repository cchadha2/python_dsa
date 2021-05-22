# Directed graph.
from undirected_graph import Graph


class DiGraph(Graph):

    def __init__(self, num_vertices, edges=()):
        super().__init__(num_vertices, edges)
        self.pre_order = []
        self._post_order = []
        self._reverse_post_order = []

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

    # TODO: Handle post order traversal iteratively.
    def dfs(self, source):
        self._pre_order.clear()
        self._post_order.clear()
        visited = set()

        stack = [source]
        current_stack = [source]
        current_vertex = None

        while stack:
            vertex = stack.pop()
            if current_stack:
                current_stack.pop()
            else:
                self._post_order.append(current_vertex)

            # Duplicate vertices can be put on stack from two different adjacent vertices. To
            # avoid an O(N) time check through stack each time we want to add an adjacent
            # vertex, we instead check here if we've previously visited a popped vertex and allow
            # duplicate vertices on the stack.
            if vertex not in visited:
                self._pre_order.append(vertex)
                visited.add(vertex)
                yield vertex

                for adjacent_vertex in self.adj[vertex]:
                    # Don't bother adding adjacent_vertex to stack if it has already been visited.
                    if adjacent_vertex not in visited:
                        stack.append(adjacent_vertex)
                        current_stack.append(adjacent_vertex)
                current_vertex = vertex

    def pre_order(self):
        return iter(self._pre_order)

    def post_order(self):
        return iter(self._post_order)

    def reverse_post_order(self):
        return reversed(self._post_order)


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
    graph.add_edge((0, 4))
    graph.add_edge((3, 5))
    print(*graph.dfs(2))
    print(*graph.bfs(2))

    print(graph)
    print(graph.reverse())

