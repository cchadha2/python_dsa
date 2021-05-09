"""Binary Search Tree implementation."""
from dataclasses import dataclass
from operator import lt, gt
from typing import Type, Union


@dataclass
class _Node:
    """A private class to hold BST data."""
    key: Union[int, str, tuple, float, bytes, frozenset]
    value: object
    left: Type["_Node"] = None
    right: Type["_Node"] = None

    def __eq__(self, key):
        return self.key == key

    def __lt__(self, key):
        return self.key < key

    def __le__(self, key):
        return self.key <= key

    def __gt__(self, key):
        return self.key > key

    def __ge__(self, key):
        return self.key >= key


class BinarySearchTree:
    """Binary Search Tree implementation."""
    def __init__(self):
        self._root = self.min = self.max = None
        self._size = 0

    def get(self, key):
        """Get value for given key."""
        node = self._root
        while node:
            if node > key:
                node = node.left
            elif node < key:
                node = node.right
            else:
                break

        if node != key:
            raise KeyError("Given key is not in tree")

        return node

    def put(self, key, value):
        """Put value at given key."""
        # node = self._get_closest(key)

        def attribute_putter(obj, attr):
            setattr(obj, attr, _Node(key, value))
            self._check_min_and_max(getattr(obj, attr))
            self._size += 1

        if not self._root:
            attribute_putter(self, "_root")
            return

        node = self._root
        while node:
            if node > key:
                if not node.left:
                    attribute_putter(node, "left")
                    return
                node = node.left

            elif node < key:
                if not node.right:
                    attribute_putter(node, "right")
                    return
                node = node.right

            else:
               node.value = value
               return

    def _check_min_and_max(self, node):
        """Compare min and max keys of tree with given node's key."""
        if not self.min or self.min > node.key:
            self.min = node

        if not self.max or self.max < node.key:
            self.max = node

    def __len__(self):
        return self._size

if __name__ == "__main__":
    tree = BinarySearchTree()

    tree.put("a", 1)
    tree.put("b", 2)
    tree.put("z", 6)

    print(len(tree))

    print(tree.get("a"))
    print(tree.get("z"))
    
    try:
        tree.get("fjsi")
    except KeyError:
        print("Caught KeyError")

    print(tree.max)
    print(tree.min)
