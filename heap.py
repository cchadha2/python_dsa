# Heap priority queue implementation.


class MaxPQ:
    """Heap (max) priority queue."""

    def __init__(self, *values):
        self.heap = values

    def push(self, item):
        self.heap.append(item)
        # Swim new item up heap.
        self._swim(-1)

    def pop(self):
        # Delete and return smallest item in heap.
        return self.heap.pop()

    def del_max(self):
        self.heap[-1], self.heap[0] = self.heap[0], self.heap[-1]
        maximum = self.pop()

        # Sink the new root to its correct position.
        self._sink(0, len(seq))

        return maximum


    def __len__(self):
        return len(self.heap)

    def _sink(self):
        

    def _swim(self):
        pass


