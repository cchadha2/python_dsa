# Undirected graph (adjacency sets representation to allow for quick checks of adjacent vertices).
# Note that this implementation forbids parallel edges but does allow for the addition of vertices.
# (as opposed to an adjacency lists representation).
import collections


class Graph:
    def __init__(self, num_vertices, edges=()):
        self.adj = [set() for _ in range(num_vertices)]

        self.num_edges = 0
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        from_vertex, to_vertex = edge
        self.adj[from_vertex].add(to_vertex)
        self.adj[to_vertex].add(from_vertex)
        self.num_edges += 1

    def add_vertex(self):
        self.adj.append(set())

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
            yield vertex

            for adjacent_vertex in self.adj[vertex]:
                if adjacent_vertex not in visited:
                    queue.append(adjacent_vertex)

            visited.add(vertex)

    def dfs(self, source):
        visited = set()

        stack = [source]
        while stack:
            vertex = stack.pop()
            yield vertex

            for adjacent_vertex in self.adj[vertex]:
                if adjacent_vertex not in visited:
                    stack.append(adjacent_vertex)

            visited.add(vertex)


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

    print(*graph.dfs(2))
    print(*graph.bfs(2))
