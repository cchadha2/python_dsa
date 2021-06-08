"""Linked List implementation."""
import functools
from dataclasses import dataclass
from typing import Type


class NoSuchElementError(Exception):
    """Used when attempting to pop from empty stack"""


@dataclass
class _Node:
    """A private class used to hold data within LinkedList."""
    value: object
    after: Type["_Node"] = None


class LinkedListIterator:
    """Iterator class for LinkedList."""
    def __init__(self, first):
        """Initialise with first value in LinkedList"""
        self.next_node = first

    def __iter__(self):
        return self

    def __next__(self):
        """Manipulate _Node references to point to next node in LinkedList."""
        if not self.next_node:
            raise StopIteration

        current_node = self.next_node
        self.next_node = current_node.after
        return current_node.value


def _add_to_empty(insert_method):
    """Used to add value when LinkedList is empty."""
    @functools.wraps(insert_method)
    def decorator(self, value):
        if self.is_empty:
            node = _Node(value)
            self._first = self._last = node
            self._size += 1
        else:
            insert_method(self, value)

    return decorator


class LinkedList:
    def __init__(self, *values):
        self._first = self._last = None
        self._size = 0

        if values:
            self._first = _Node(values[0])
            self._last = self._first
            self._size += 1
            for value in values[1:]:
                self.append(value)

    @property
    def is_empty(self):
        return self._size == 0

    @_add_to_empty
    def append(self, value):
        """Append given value to end of LinkedList."""
        node = _Node(value)

        self._last.after = node
        self._last = node
        self._size += 1

    @_add_to_empty
    def insert_first(self, value):
        """Insert given value at start of LinkedList"""
        node = _Node(value)
        node.after = self._first
        self._first = node
        self._size += 1

    def insert_after(self, value, to_insert):
        """Insert a given value after another value (if the other value exists)."""
        node = self._get(value)
        node_to_insert = _Node(to_insert)

        if not node.after:
            node.after = node_to_insert
        else:
            node_to_insert.after = node.after
            node.after = node_to_insert

        self._size += 1

    def extend(self, values):
        """Extend the LinkedList given an iterable `values`."""
        for value in values:
            self.append(value)

    def remove(self, value):
        """Remove first occurrence of given value from LinkedList."""
        self._raise_empty_error()

        node = self._first
        if node.value == value:
            self.remove_first()
            return

        while node.after:
            if node.after.value == value:
                node.after = node.after.after
                self._size -= 1
                return

            node = node.after

    def remove_first(self):
        """Remove first value in LinkedList and return."""
        self._raise_empty_error()

        node = self._first
        if node.after:
            self._first = node.after
        else:
            self._first = None

        self._size -= 1

        return node.value

    def remove_after(self, value):
        """Remove value after given value and return."""
        self._raise_empty_error()

        node = self._get(value)

        if not node.after:
            raise NoSuchElementError("No value after given value.")

        to_return = node.after
        node.after = to_return.after

        self._size -= 1

        return to_return.value

    def _raise_empty_error(self):
        """Raise a ValueError if LinkedList is empty."""
        if self.is_empty:
            raise NoSuchElementError("No values in LinkedList.")

    def _get(self, value):
        """Get a _Node object with the given value."""
        node = self._first
        while node:
            if node.value == value:
                return node
            node = node.after

        raise NoSuchElementError(f"Given value ({value}) does not exist in LinkedList.")

    def __contains__(self, value):
        try:
            self._get(value)
        except NoSuchElementError:
            return False
        else:
            return True

    def __iter__(self):
        # Can return an object of LinkedListIterator but more pythonic to use a generator as
        # __iter__ will simply return a generator object which already has an __iter__ and
        # __next__ method.
        # return LinkedListIterator(self._first)

        # Generator implementation.
        next_node = self._first

        while next_node:
            current_node = next_node
            next_node = current_node.after
            yield current_node.value

    def __str__(self):
        return f"[{', '.join(str(elem) for elem in self.__iter__())}]"

    def __len__(self):
        return self._size


if __name__ == '__main__':
    linked_list = LinkedList(1, 2, 3, 4)

    print(linked_list)
    print(len(linked_list))

    linked_list.append(5)
    print(linked_list)
    print(len(linked_list))

    value = linked_list.remove_first()
    print(value)
    print(linked_list)
    print(len(linked_list))


    value = linked_list.remove_after(3)
    print(value)
    print(linked_list)
    print(len(linked_list))

    linked_list.insert_after(3, value)
    print(linked_list)
    print(len(linked_list))

    linked_list.insert_first(1)
    print(linked_list)
    print(len(linked_list))

    print(1 in linked_list)

    print(linked_list.__iter__())
    print(next(linked_list.__iter__()))
    for elem in linked_list:
        print(elem)

    print(linked_list.is_empty)
    print(len(linked_list))

    while linked_list:
        linked_list.remove_first()

    print(linked_list)
    print(len(linked_list))

    linked_list.append(154)
    print(linked_list)
    print(len(linked_list))

    new_linked_list = LinkedList()

    print(new_linked_list.is_empty)

    new_linked_list.insert_first(54)
    print(new_linked_list)
    print(len(new_linked_list))

    new_linked_list.extend((1, 4, 7, 3, 1))
    print(new_linked_list)
    print(len(new_linked_list))

    try:
        linked_list.insert_after("hello", 4)
    except NoSuchElementError:
        pass
    else:
        print("One of these didn't raise correctly hmmm")

    try:
        LinkedList().remove_first()
    except NoSuchElementError:
        pass
    else:
        print("One of these didn't raise correctly hmmm")

    try:
        linked_list.remove_after("hey buuuuddy")
    except NoSuchElementError:
        pass
    else:
        print("One of these didn't raise correctly hmmm")

    print(linked_list)
    print("hello" in linked_list)

    linked_list.extend([6, 5, 1, 2, 3])
    print(linked_list, len(linked_list))

    linked_list.remove(1)
    print(linked_list, len(linked_list))



