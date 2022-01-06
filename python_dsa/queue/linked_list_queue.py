# Queue implementation with deque.
from python_dsa.linked_list import LinkedList, NoSuchElementError


class Queue(LinkedList):

    def __init__(self, *values):
        super().__init__(*values)

    def enqueue(self, value):
        self.append(value)

    def dequeue(self):
        return self.remove_first()

    def peek(self):
        if self.is_empty:
            raise NoSuchElementError("Queue is empty")

        return self._first.value


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

