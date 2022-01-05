# Topological sort with recursive digraph.
from graph.directed_graph_recursive import DiGraphRecursive
from .directed_cycle import DirectedCycle
from .depth_first_order_recursive import DepthFirstOrder


class Topological(DiGraphRecursive):

    def __init__(self, num_vertices, edges=()):
        super().__init__(num_vertices, edges)

        self.order = ()
        # Could be made more efficient by taking the directed graph itself as input to initializers
        # of each of these classes instead of reconstructing.
        cycle_finder = DirectedCycle(num_vertices, edges)
        if not cycle_finder.has_cycle():
            dfs = DepthFirstOrder(num_vertices, edges)
            self.order = tuple(dfs.reverse_post_order())

    def __iter__(self):
        return iter(self.order)

    def has_order(self):
        return bool(self.order)


if __name__ == "__main__":
    graph = Topological(7, edges=((0, 4), (2, 5), (2, 4), (2, 3), (3, 5), (4, 3), (4, 1), (5, 0), (1, 6), (1, 0)))
    print(graph)
    print(graph.has_order())
    print(*graph)

    # Example input from Algorithms book (pg. 579).
    graph = Topological(13, edges=((2, 0), (0, 5), (0, 1), (0, 6), (2, 3), (3, 5), (5, 4), (6, 4),
                                     (7, 6), (8, 7), (6, 9), (9, 11), (9, 10), (9, 12), (11, 12)))
    print(graph)
    print(graph.has_order())
    print(*graph)

