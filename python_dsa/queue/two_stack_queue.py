# Queue implementation with two stacks.
from linked_list import NoSuchElementError


class Queue:

    def __init__(self, *items):
        self.enqueue_stack = list(items)
        self.dequeue_stack = []

        while self.enqueue_stack:
            self.dequeue_stack.append(self.enqueue_stack.pop())

    def enqueue(self, val):
        self.enqueue_stack.append(val)

    def dequeue(self):
        if self.is_empty:
            raise NoSuchElementError("Nothing on the queue")

        if not self.dequeue_stack:

            while self.enqueue_stack:
                self.dequeue_stack.append(self.enqueue_stack.pop())

        return self.dequeue_stack.pop()

    def peek(self):
        if self.is_empty:
            raise NoSuchElementError("Nothing on the queue")

        return self.dequeue_stack[-1] if self.dequeue_stack else self.enqueue_stack[0]

    @property
    def is_empty(self):
        return not self.dequeue_stack and not self.enqueue_stack

    def __len__(self):
        return len(self.dequeue_stack) + len(self.enqueue_stack)

    def __iter__(self):
        for elem in reversed(self.dequeue_stack):
            yield elem

        for elem in self.enqueue_stack:
            yield elem

    def __repr__(self):
        return f"[{', '.join(str(elem) for elem in self)}]"

    __str__ = __repr__


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

