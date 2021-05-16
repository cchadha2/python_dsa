# Linked list implementation of stack.
import functools
from linked_list import LinkedList, NoSuchElementError


def check_empty(method):
    @functools.wraps(method)
    def inner_func(self):
        if self.is_empty:
            raise NoSuchElementError("Container is empty")
        return method(self)
    return inner_func


# Stack implementation inheriting from LinkedList (as opposed to resizing stack composition
# relationship)
class Stack(LinkedList):

    def __init__(self, *items):
        super().__init__(*reversed(items))

    def push(self, item):
        self.insert_first(item)

    @check_empty
    def pop(self):
        return self.remove_first()

    @check_empty
    def peek(self):
        return self._first.value


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
        print("Pop works correctly with empty stack")

