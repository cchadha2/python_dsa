"""Binary Search Tree implementation."""
from dataclasses import dataclass
from operator import lt, gt
from typing import Type, Union


@dataclass
class _Node:
    """A private class to hold BST data."""
    # All standard immutable types.
    key: Union[int, str, tuple, float, bytes, frozenset]
    value: object
    left: Type["_Node"] = None
    right: Type["_Node"] = None

    def __eq__(self, key):
        return self.key == key

    def __lt__(self, key):
        return self.key < key

    def __gt__(self, key):
        return self.key > key

class BinarySearchTree:
    """Binary Search Tree iterative implementation to avoid Python's recursion limit."""
    def __init__(self):
        self._root = None
        self._size = 0
        self._keys = set()

    @property
    def min(self):
        _, minimum = self._check_extreme("left")
        return minimum.key

    @property
    def max(self):
        _, maximum = self._check_extreme("right")
        return maximum.key

    def floor(self, key):
        """Find largest key smaller than or equal to `key`"""
        return self._closest(key, direction="left").key

    def ceiling(self, key):
        """Find smallest key larger than or equal to `key`"""
        return self._closest(key, direction="right").key

    # TODO: Finish this correctly (by navigating tree).
    def rank(self, key):
        """Find number of keys less than key."""
        closest = self._closest(key, direction="left")
        if not closest:
            return 0

        # Initialise number of keys based on whether the closest node found
        # is the node with key `key`.
        num = 0 if closest.key == key else 1

        return len(tuple(self.keys(self.min, key)))

    def delete_min(self):
        """Delete minimum node in tree."""
        extreme = self._delete_extreme("left")
        return extreme if not extreme else extreme.key

    def delete_max(self):
        """Delete maximum node in tree."""
        extreme = self._delete_extreme("right")
        return extreme if not extreme else extreme.key

    # TODO: This should navigate the tree itself to save time.
    def keys(self, minimum, maximum):
        """Find keys between minimum and maximum keys (inclusive)."""
        for key in self._keys:
            if key >= minimum and key <= maximum:
                yield key

    def _get(self, key):
        """Get node for given key."""
        node = self._root
        while node:
            if node > key:
                node = node.left
            elif node < key:
                node = node.right
            else:
                break

        if node != key:
            raise KeyError("given key is not in tree")

        return node

    def _put(self, key, value):
        """Put value at given key."""
        def put_node(obj, attr):
            """Put node in tree."""
            setattr(obj, attr, _Node(key, value))
            self._keys.add(key)
            self._size += 1

        if not self._root:
            put_node(self, "_root")
            return

        node = self._root
        while node:
            if node > key:
                if not node.left:
                    put_node(node, "left")
                    return
                node = node.left
            elif node < key:
                if not node.right:
                    put_node(node, "right")
                    return
                node = node.right
            else:
               node.value = value
               return

    def _delete(self, key):
        """Delete node at given key."""
        def delete_node(parent, side, node):
            """Delete node from tree."""
            if node.right:
                setattr(parent, side, node.right)
                setattr(parent, side + ".left", node.left)
            elif node.left:
                setattr(parent, side, node.left)
            else:
                setattr(parent, side, None)

            self._keys.remove(key)
            self._size -= 1

        node = self._root

        while node:
            if node > key:
                next_node = node.left
                if next_node == key:
                    delete_node(node, "left", next_node)
                    return
                node = next_node
            elif node < key:
                next_node = node.right
                if next_node == key:
                    delete_node(node, "right", next_node)
                    return
                node = next_node
            else:
                delete_node(self, "_root", node)
                return

    def _closest(self, key, direction):
        """Find closest key larger/smaller than or equal to `key`"""
        if direction == "left":
            other_direction = "right"
            operator, other_operator = gt, lt
        else:
            other_direction = "left"
            operator, other_operator = lt, gt

        node = self._root
        closest = None
        while node:
            if operator(node, key):
               node = getattr(node, direction)
            elif other_operator(node, key):
                if not closest or operator(node, closest.key):
                    closest = node
                node = getattr(node, other_direction)
            else:
                return closest

        return closest

    def _delete_extreme(self, direction):
        if not self._root:
            return

        extreme = self._root
        other_direction = "right" if direction == "left" else "left"

        # Check if node to be deleted is the root node.
        if self._size == 1 or not getattr(self._root, direction):
            extreme = self._root
            self._root = getattr(self._root, other_direction, None)
            self._size -= 1
            self._keys.remove(extreme.key)
            return extreme

        # Otherwise delete the extreme node.
        parent, extreme = self._check_extreme(direction)
        setattr(parent, direction, getattr(extreme, other_direction))
        self._size -= 1
        self._keys.remove(extreme.key)

        return extreme

    def _check_extreme(self, direction):
        """Find min or max node in tree"""
        extreme = self._root
        parent = None
        while getattr(extreme, direction):
            parent = extreme
            extreme = getattr(extreme, direction)

        return parent, extreme

    def __getitem__(self, key):
        """Get value for given key."""
        return self._get(key)

    def __setitem__(self, key, value):
        """Set value at given key."""
        self._put(key, value)

    def __delitem__(self, key):
        """Delete item at given key"""
        self._delete(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        return iter(self._keys)

    def __contains__(self, key):
        return key in self._keys

if __name__ == "__main__":
    tree = BinarySearchTree()

    tree["a"] =  1
    tree["b"] =  2
    tree["z"] =  6

    print(len(tree))

    print(tree["a"])
    print(tree["z"])

    try:
        tree["fjsi"]
    except KeyError:
        print("Caught KeyError")

    print(tree.max)
    print(tree.min)

    tree["c"] =  965
    tree["f"] =  3252
    tree["t"] =  2345
    tree["v"] =  3754
    tree["m"] =  657

    print(len(tree))
    print(tree.max)
    print(tree.min)
    print()

    for key in tree.keys("b", "t"):
        print(key)

    print("Floor of 'n': ", tree.floor("n"))
    print("Ceiling of 'n': ", tree.ceiling("n"))
    print(tree.floor("v"))
    print(tree.ceiling("v"))
    print(*tree)

    del tree["v"]
    print(*tree)
    try:
        tree["v"]
    except KeyError:
        print("v has been successfully deleted")

    print(len(tree))
    print(tree.delete_min())
    try:
        print(tree["a"])
    except KeyError:
        print("a has been successfully deleted")
        print(len(tree))
        print(*tree)
    else:
        print("a was not deleted!")

    print(tree.delete_max())
    try:
        print(tree["z"])
    except KeyError:
        print("z has been successfully deleted")
        print(len(tree))
        print(*tree)
    else:
        print("z was not deleted!")
    tree = BinarySearchTree()
    tree["a"] =  1
    print(len(tree))

    del tree["a"]
    print(len(tree))
    print(*tree)
    print("a" in tree)
    print(tree.delete_max())
    tree["a"] =  1
    print(tree.delete_max())
    tree["a"] =  1
    print(tree.delete_min())
    print(*tree)

