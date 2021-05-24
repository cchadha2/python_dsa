# Directed graph.
from undirected_graph import Graph


class DiGraph(Graph):

    def add_edge(self, edge):
        """Same as Graph but only add edge in a single direction."""
        from_vertex, to_vertex = edge
        self.adj[from_vertex].append(to_vertex)
        self.num_edges += 1

    def reverse(self):
        """Returns a new DiGraph with directions reversed."""
        reverse_digraph = DiGraph(self.num_vertices)
        for idx, vertex in enumerate(self.adj):
            for to_vertex in vertex:
                reverse_digraph.add_edge((to_vertex, idx))

        return reverse_digraph

    def dfs(self, source):
        stack = [source]
        visited = set()

        while stack:
            vertex = stack.pop()

            # Duplicate vertices can be put on stack from two different adjacent vertices. To
            # avoid an O(N) time check through stack each time we want to add an adjacent
            # vertex, we instead check here if we've previously visited a popped vertex and allow
            # duplicate vertices on the stack.
            if vertex not in visited:
                visited.add(vertex)
                yield vertex

                for adjacent_vertex in self.adj[vertex]:
                    # Don't bother adding adjacent_vertex to stack if it has already been visited.
                    if adjacent_vertex not in visited:
                        stack.append(adjacent_vertex)


if __name__ == "__main__":
    graph = DiGraph(6, edges=((2, 5), (2, 4), (2, 3), (4, 3), (4, 1), (5, 0), (1, 0)))
    print(graph)

    print(graph.num_edges)
    print(graph.num_vertices)

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

