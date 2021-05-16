# Stack implementations with Python list
from linked_list import NoSuchElementError


# Resizing stack using a Python list in a composition relationship.
class Stack:
    def __init__(self, *items):
        self._stack = []
        self._stack.extend(items)

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        if not self._stack:
            raise NoSuchElementError("Stack is empty")

        return self._stack.pop()

    def peek(self):
        if not self._stack:
            raise NoSuchElementError("Stack is empty")

        return self._stack[-1]

    @property
    def is_empty(self):
        return len(self._stack) == 0

    def __len__(self):
        return len(self._stack)

    def __iter__(self):
        # Iterates over stack in FILO order.
        return reversed(self._stack)

    def __str__(self):
       return str(self._stack)


if __name__ == "__main__":
    stack = Stack(1, 2, 3)
    print(stack)

    stack.push(4)
    print(stack)

    print(stack.peek())
    print(stack.pop())
    print(stack)

    print(stack.is_empty)
    print(len(stack))

    for elem in stack:
        print(elem)

    new_stack = Stack()
    print(new_stack.is_empty)

    try:
        new_stack.pop()
    except NoSuchElementError:
        print("Pop works correctly with empty stack")
    try:
        new_stack.peek()
    except NoSuchElementError:
        print("Peek works correctly with empty stack")

