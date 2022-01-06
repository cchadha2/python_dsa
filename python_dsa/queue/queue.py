# Queue implementation with deque.
from collections import deque

from python_dsa.linked_list import NoSuchElementError


class Queue:

    def __init__(self, *values):
        self._queue = deque(values)

    def enqueue(self, value):
        self._queue.append(value)

    def dequeue(self):
        if not self._queue:
            raise NoSuchElementError("Queue is empty")

        return self._queue.popleft()

    def peek(self):
        if not self._queue:
            raise NoSuchElementError("Queue is empty")

        return self._queue[0]

    @property
    def is_empty(self):
        return not self._queue

    def __len__(self):
        return len(self._queue)

    def __iter__(self):
        # Iterate over queue in FIFO order.
        return iter(self._queue)

    def __str__(self):
        return f"[{', '.join(str(value) for value in self._queue)}]"


if __name__ == "__main__":
    queue = Queue(1, 2, 3)
    print(queue)

    queue.enqueue(4)
    print(queue)

    print(queue.peek())
    print(queue.dequeue())
    print(queue)

    print(queue.is_empty)
    print(len(queue))

    for elem in queue:
        print(elem)

    new_queue = Queue()
    print(new_queue.is_empty)

    try:
        new_queue.dequeue()
    except NoSuchElementError:
        print("Dequeue works correctly with empty queue")
    try:
        new_queue.peek()
    except NoSuchElementError:
        print("Peek works correctly with empty queue")

