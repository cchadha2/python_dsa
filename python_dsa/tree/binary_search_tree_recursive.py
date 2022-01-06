"""Binary Search Tree implementation."""
from collections import deque
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
    size: int = 1

    def __eq__(self, key):
        return self.key == key

    def __lt__(self, key):
        return self.key < key

    def __gt__(self, key):
        return self.key > key

    def __le__(self, key):
        return self.key <= key

    def __ge__(self, key):
        return self.key >= key


class BinarySearchTree:
    """Binary Search Tree traditional recursive implementation."""

    def __init__(self):
        self._root = None

    def __getitem__(self, key):
        """Get value for given key."""
        node = self._get(self._root, key)
        if not node:
            raise KeyError("Given key not in tree")

        return node.value

    def __setitem__(self, key, value):
        """Set value at given key."""
        self._root = self._put(self._root, key, value)

    def __delitem__(self, key):
        """Delete item at given key"""
        self._root = self._delete(self._root, key)

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.in_order()

    def __repr__(self):
        return f"BinarySearchTree(root={self._root})"

    def __contains__(self, key):
        return bool(self._get(self._root, key))

    @property
    def size(self):
        return self._size(self._root)

    @property
    def min(self):
        return self._min(self._root).key

    @property
    def max(self):
        return self._max(self._root).key

    def floor(self, key):
        """Find largest key smaller than or equal to `key`"""

        def find_node(node, key):
            if not node:
                return

            if node == key:
                return node
            elif node < key:
                return find_node(node.right, key) or node

            return find_node(node.left, key)

        res = find_node(self._root, key)
        if not res:
            raise ValueError("No such element in tree")

        return res

    def ceiling(self, key):
        """Find smallest key larger than or equal to `key`"""

        def find_node(node, key):
            if not node:
                return

            if node == key:
                return node
            elif node > key:
                return find_node(node.left, key) or node

            return find_node(node.right, key)

        res = find_node(self._root, key)
        if not res:
            raise ValueError("No such element in tree")

        return res

    def rank(self, key):
        """Find number of keys less than key."""
        #return sum(map(lambda node: node < key, iter(self)))

        def _rank(node, key):
            if not node:
                return 0

            if node > key:
                return _rank(node.left, key)
            elif node < key:
                return self._size(node.left) + 1 + _rank(node.right, key)

            return self._size(node.left)

        return _rank(self._root, key)


    def select(self, rank):
        """Find key with specified rank"""
        if rank >= self.size:
            raise ValueError("Not enough elements to find a key with this rank")
        elif rank <= 0:
            raise ValueError("Invalid rank specified")

        def _select(node, rank):
            if not node:
                return

            curr_rank = self._size(node.left)
            # If the current rank is greater than the specified rank,
            # we need to look to the left.
            if curr_rank > rank:
                return _select(node.left, rank)
            # If the current rank is lower, then we need to look to the
            # right where all nodes are greater than the current node
            # so we subtract the number of nodes less than the current
            # node and the current node itself from the rank we want to find.
            elif curr_rank < rank:
                return _select(node.right, rank - curr_rank - 1)
            
            return node
        
        return _select(self._root, rank)

    def delete_min(self):
        """Delete minimum node in tree."""
        if not self._root:
            raise ValueError("Tree is empty")

        self._root = self._delete_min(self._root)

    def delete_max(self):
        """Delete maximum node in tree."""
        if not self._root:
            raise ValueError("Tree is empty")

        self._root = self._delete_max(self._root)

    def keys(self, minimum=None, maximum=None):
        """Find keys between minimum and maximum keys (inclusive)."""
        if minimum is None and maximum is None:
            return list(self)
        elif (minimum and not maximum) or (not minimum and maximum):
            raise ValueError("Both minimum and maximum must be set or neither")
        else:
            return list(self._generate_keys(self._root, minimum, maximum))

    # TODO: Implement recursive BFS.
    def bfs(self):
        """Breadth-first traversal of tree"""
        if not self._root:
            raise ValueError("No keys in tree")

        queue = deque()
        queue.append(self._root)
        while queue:
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            yield node.key

    def pre_order(self):
        """Pre-order traversal of tree."""

        def traverse(node):
            if not node:
                return

            yield node.key

            yield from traverse(node.left)

            yield from traverse(node.right)

        return traverse(self._root)

    def in_order(self):
        """In-order traversal of tree."""

        def traverse(node):
            if not node:
                return

            yield from traverse(node.left)

            yield node.key

            yield from traverse(node.right)

        return traverse(self._root)

    def post_order(self):
        """Post-order traversal of tree."""

        def traverse(node):
            if not node:
                return

            yield from traverse(node.left)

            yield from traverse(node.right)

            yield node.key

        return traverse(self._root)

    def _size(self, node):
        return node.size if node else 0

    def _generate_keys(self, node, minimum, maximum):
        """Recursive generator of keys in range provided."""
        if not node:
            return

        if node > minimum:
            yield from self._generate_keys(node.left, minimum, maximum)

        if minimum <= node < maximum:
            yield node.key

        if node < maximum:
            yield from self._generate_keys(node.right, minimum, maximum)

    def _get(self, node, key):
        """Get node for given key."""
        if not node:
            return

        if node > key:
            return self._get(node.left, key)
        elif node < key:
            return self._get(node.right, key)

        return node

    def _put(self, node, key, value):
        """Put value at given key."""
        if not node:
            return _Node(key, value)

        if key < node:
            node.left = self._put(node.left, key, value)
        elif key > node:
            node.right = self._put(node.right, key, value)
        else:
           node.value = value

        node.size = self._size(node.left) + 1 + self._size(node.right)
        return node

    def _delete(self, node, key):
        """Delete node at given key."""
        if not node:
            return

        if key < node:
            node.left = self._delete(node.left, key)
        elif key > node:
            node.right = self._delete(node.right, key)
        else:
            if not node.right:
                return node.left
            elif not node.left:
                return node.right

            node_to_delete = node
            # Find the successor and delete it from the right subtree.
            node = self._min(node_to_delete.right)
            node.right = self._delete_min(node_to_delete.right)
            # Set the left child to the original node's left child.
            node.left = node_to_delete.left

        node.size = self._size(node.left) + 1 + self._size(node.right)
        return node

    def _delete_min(self, node):
        if not node.left:
            return node.right

        node.left = self._delete_min(node.left)
        node.size = self._size(node.left) + 1 + self._size(node.right)
        return node

    def _delete_max(self, node):
        if not node.right:
            return node.left

        node.right = self._delete_max(node.right)
        node.size = self._size(node.left) + 1 + self._size(node.right)
        return node

    def _min(self, node):
        """Find min node in tree"""
        if not node.left:
            return node

        return self._min(node.left)

    def _max(self, node):
        """Find max node in tree"""
        if not node.right:
            return node

        return self._max(node.right)


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
    print("Tree keys in iterator: ", *tree)

    del tree["v"]

    print(*tree)
    try:
        tree["v"]
    except KeyError:
        print("v has been successfully deleted")
    else:
        print("v was not deleted")
    print(tree.keys())

    print(len(tree))
    print(tree.delete_min())
    try:
        print(tree["a"])
    except KeyError:
        print("a has been successfully deleted")
        print(len(tree))
    else:
        print("a was not deleted!")

    print(*tree)
    print(f"rank of 'm': {tree.rank('m')}")
    print(f"key with rank 3: {tree.select(3)}")
    print(tree.select(5))
    print(tree.select(1))

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
    print(tree._root)
    print(len(tree))

    del tree["a"]
    print(tree)
    print(len(tree))
    print(*tree)
    print("a" in tree)
    try:
        print(tree.delete_max())
    except ValueError:
        print(tree)
        print("delete_max is a-ok")
    else:
        print("delete_max not working right!")

    print(tree.size)

    tree["a"] =  1
    print(tree.size)
    print(tree.delete_max())

    tree["a"] =  1
    print(tree.size)
    print(tree.delete_min())
    print(tree.size)
    print(*tree)

    try:
        list(tree.keys("a"))
    except ValueError:
        print("keys method raised ValueError correctly")


    tree = BinarySearchTree()
    for value, key in enumerate(("b", "a", "z", "v", "e", "f")):
        tree[key] = value

    print(*tree)

    print(tree)
    print(vars(tree))
    del tree["b"]
    print(vars(tree))

    print(tree)
    for key in tree.keys():
        print(f"Key to delete is {key}")
        print(tree[key])
        print(vars(tree))
        del tree[key]
        print(f"{key=} was deleted")
        print(vars(tree))

    print(len(tree))


    tree = BinarySearchTree()
    for value, key in enumerate(('m', 'g', 's', 'd', 'j', 'p', 'w', 'b', 'f', 'h', 'k', 'o', 'r',
                                 'u', 'z')):
        tree[key] = value

    for key in tree.bfs():
        print(key)

    print()

    for key in tree.pre_order():
        print(key)

