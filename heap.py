# Heap priority queue implementation.
class MaxPQ:
    """Heap (max) priority queue."""

    def __init__(self, *values):
        self._heap = []
        for value in values:
            self.push(value)

    def push(self, item):
        self._heap.append(item)
        # Swim new item up heap.
        self._swim(len(self._heap) - 1)

    def del_max(self):
        self._heap[-1], self._heap[0] = self._heap[0], self._heap[-1]
        maximum = self._heap.pop()

        # Sink the new root to its correct position.
        self._sink(0)

        return maximum

    def __len__(self):
        return len(self._heap)

    def _sink(self, idx):
        """Sink value to its correct position in priority queue."""
        # For zero-indexed heap, the first child of idx is at 2 * (idx + 1).
        while 2 * (idx + 1) - 1 <= len(self._heap) - 1:
            child_idx = 2 * (idx + 1) - 1
            # If the child index is within the heap and its value is less than its sibling (the
            # other child) then increment the child index to the next child index.
            if (child_idx < len(self._heap) - 1
                    and self._heap[child_idx] < self._heap[child_idx + 1]):
                child_idx += 1
            # If the current index value is not less than the child index value then the current
            # index value is in the correct place.
            if not self._heap[idx] < self._heap[child_idx]:
                break

            self._heap[idx], self._heap[child_idx] = self._heap[child_idx], self._heap[idx]
            idx = child_idx

    def _swim(self, idx):
        """Swim value to its correct position in priority queue."""
        while idx > 0 and self._heap[(idx - 1) // 2] < self._heap[idx]:
            self._heap[(idx - 1) // 2], self._heap[idx] = self._heap[idx], self._heap[(idx - 1) // 2]
            idx = (idx - 1) // 2

    def __str__(self):
        return str(self._heap)


if __name__ == "__main__":
    pq = MaxPQ('h', 'i', 'e', 's', 'r', 't', 'g', 'a', 'o', 'p', 'n')
    print(pq)

    print(len(pq))

    while pq:
        print(pq.del_max())

    pq = MaxPQ('h', 'i', 'e', 's', 'r', 't', 'g', 'a', 'o', 'p', 'n')
    pq.push('j')
    print(pq)
    print(len(pq))

