# Undirected graph (adjacency lists representation).
import collections


class Graph:
    def __init__(self, num_vertices, edges=()):
        self.adj = [[] for _ in range(num_vertices)]

        self.num_edges = 0
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        from_vertex, to_vertex = edge
        self.adj[from_vertex].append(to_vertex)
        self.adj[to_vertex].append(from_vertex)
        self.num_edges += 1

    def add_vertex(self):
        self.adj.append([])

    @property
    def num_vertices(self):
        return len(self.adj)

    def edges(self, vertex):
        return iter(self.adj[vertex])

    def bfs(self, source):
        visited = set()

        queue = collections.deque()
        queue.append(source)
        while queue:
            vertex = queue.popleft()
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
                        queue.append(adjacent_vertex)



    def dfs(self, source):
        visited = set()
        stack = [source]

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

    def __str__(self):
        return str(self.adj)


if __name__ == "__main__":
    graph = Graph(5, ((0, 1), (2, 3), (4, 2)))
    print(graph)

    for edge in graph.edges(2):
        print(edge)

    print(graph.num_vertices)
    print(graph.num_edges)

    graph.add_edge((4, 1))
    print(graph.num_edges)
    print(graph)

    graph.add_vertex()
    print(graph)
    graph.add_edge((5, 2))
    print(graph)
    print(graph.num_vertices)
    print(graph.num_edges)

    graph.add_edge((5, 0))
    # graph.add_edge((4, 3))
    print(*graph.dfs(2))
    print(*graph.bfs(2))

