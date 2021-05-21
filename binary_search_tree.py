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
    """Binary Search Tree (mostly) iterative implementation to avoid Python's recursion limit.

    Python's recursion limit is set to 1000 by default. If each operation in
    this data structure is O(logN) => 2**1000 calls to reach the limit (a 302 decimal
    digit number) where N is the number of nodes in the tree. This means that this limit will
    likely never be reached. However, just to be extra super duper safe, (most) methods here
    are implemented iteratively in O(logN) time. Note that `select` is made inefficient
    due to this design choice and `keys` deviates from the design as it required
    a recursive implementation.
    """
    def __new__(cls, *args, **kwargs):
        instance = super(BinarySearchTree, cls).__new__(cls, *args, **kwargs)
        instance._root = None
        instance._size = 0
        instance._keys = set()
        return instance

    def __getitem__(self, key):
        """Get value for given key."""
        _, node_key = self._get(key)
        return node_key

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

    @property
    def min(self):
        _, minimum = self._check_extreme(self._root, "left")
        return minimum.key

    @property
    def max(self):
        _, maximum = self._check_extreme(self._root, "right")
        return maximum.key
    def floor(self, key):
        """Find largest key smaller than or equal to `key`"""
        return self._closest(key, direction="left").key

    def ceiling(self, key):
        """Find smallest key larger than or equal to `key`"""
        return self._closest(key, direction="right").key

    def rank(self, key):
        """Find number of keys less than key."""
        # Initialise number of keys to remove from final result
        # based on whether `key` is in the tree.
        num = 1 if key in self._keys else 0

        # Remove the key itself from number of keys.
        return len(self.keys(self.min, key)) - num

    def select(self, rank):
        """Find key with specified rank...in O((logN)**2) time :("""
        if rank >= self._size:
            raise ValueError("Rank exceeds number of items in tree")

        # Doing this iteratively, requires a O(logN) operation to find
        # rank of each node as we traverse the tree. This would be optimised
        # by keeping track of the number of nodes in each subtree (on the _Node class itself)
        # but would require recursive implementations of put and delete to update the sizes
        # as they go.
        node = self._root
        while node:
            node_rank = self.rank(node.key)
            if node_rank > rank:
                node = node.left
            elif node_rank < rank:
                node = node.right
            else:
                return node.key

    def delete_min(self):
        """Delete minimum node in tree."""
        extreme = self._delete_extreme(self._root, "left")
        self._size -= 1
        self._keys.remove(extreme.key)
        return extreme if not extreme else extreme.key

    def delete_max(self):
        """Delete maximum node in tree."""
        extreme = self._delete_extreme(self._root, "right")
        self._size -= 1
        self._keys.remove(extreme.key)
        return extreme if not extreme else extreme.key

    def keys(self, minimum=None, maximum=None):
        """Find keys between minimum and maximum keys (inclusive).

        This is a recursive method unfortunately :(
        """
        if minimum is None and maximum is None:
            return list(self._generate_keys(self._root, self.min, self.max))
        elif (minimum is not None and maximum is None) or (minimum is None and maximum is not None):
            raise ValueError("Both minimum and maximum must be set or neither")
        else:
            return list(self._generate_keys(self._root, minimum, maximum))

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

    def dfs(self):
        """Depth-first traversal of tree."""
        if not self._root:
            raise ValueError("No keys in tree")

        stack = [self._root]
        while stack:
            node = stack.pop()
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
            yield node.key

    def _generate_keys(self, node, minimum, maximum):
        """Recursive generator of keys in range provided."""
        if not node:
            return

        if node > minimum:
            yield from self._generate_keys(node.left, minimum, maximum)
        if node >= minimum and node <= maximum:
            yield node.key
        if node < maximum:
            yield from self._generate_keys(node.right, minimum, maximum)

    def _get(self, key):
        """Get node for given key."""
        # Parent is used by _delete method to update links.
        parent = None
        node = self._root
        while node:
            if node > key:
                parent = node
                node = node.left
            elif node < key:
                parent = node
                node = node.right
            else:
                break

        if node != key:
            raise KeyError("given key is not in tree")

        return parent, node

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
        if self._size == 1:
            self.delete_min()
            return

        def remove_node(node, direction, parent=None):
            self._size -= 1
            self._keys.remove(node.key)
            if parent:
                node = getattr(node, direction)
                setattr(parent, direction, node)
            else:
                self._root = getattr(self._root, direction)

        parent, node_to_delete = self._get(key)
        if parent is None or parent.right == node_to_delete:
            if not node_to_delete.left:
                remove_node(node_to_delete, "right", parent)
                return
            elif not node_to_delete.right:
                remove_node(node_to_delete, "left", parent)
                return
        else:
            if not node_to_delete.left:
                remove_node(node_to_delete, "left", parent)
                return
            elif not node_to_delete.right:
                remove_node(node_to_delete, "right", parent)
                return

        # The successor of the node to delete is the smallest node in its right subtree.
        successor = self._delete_extreme(node_to_delete.right, "left", parent=node_to_delete)
        successor.left, successor.right = node_to_delete.left, node_to_delete.right

        if parent:
            if parent.right == node_to_delete:
                parent.right = successor
            else:
                parent.left = successor
            self._size -= 1
            self._keys.remove(parent.key)
        else:
            self._size -= 1
            self._keys.remove(self._root.key)
            self._root = successor

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
                return node

        return closest

    def _delete_extreme(self, node, direction, parent=None):
        if not self._size:
            raise ValueError("Tree is empty")

        if not node:
            return

        # Check which way to go.
        other_direction = "right" if direction == "left" else "left"

        # Check if node to be deleted is the root node.
        if self._size == 1 or (node == self._root.key and not getattr(node, direction)):
            extreme = self._root
            self._root = getattr(node, other_direction, None)
            return extreme

        # Otherwise delete the extreme node.
        parent, extreme = self._check_extreme(node, direction, parent)
        setattr(parent, direction, getattr(extreme, other_direction))
        return extreme

    def _check_extreme(self, node, direction, parent=None):
        """Find min or max node in tree"""
        while getattr(node, direction):
            parent = node
            node = getattr(node, direction)

        return parent, node


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
    print(len(tree))
    print(*tree)
    print("a" in tree)
    try:
        print(tree.delete_max())
    except ValueError:
        print("delete_max is a-ok")
    else:
        print("delete_max not working right!")

    print(tree._size)

    tree["a"] =  1
    print(tree._size)
    print(tree.delete_max())

    tree["a"] =  1
    print(tree._size)
    print(tree.delete_min())
    print(tree._size)
    print(*tree)

    try:
        list(tree.keys("a"))
    except ValueError:
        print("keys method raised ValueError correctly")


    tree = BinarySearchTree()
    for value, key in enumerate(("b", "a", "z", "v", "e", "f")):
        tree[key] = value

    print(*tree)

    del tree["b"]
    print(vars(tree))

    for key in tree.keys():
        print(tree[key])
        print(vars(tree))
        del tree[key]

    print(len(tree))


    tree = BinarySearchTree()
    for value, key in enumerate(('m', 'g', 's', 'd', 'j', 'p', 'w', 'b', 'f', 'h', 'k', 'o', 'r',
                                 'u', 'z')):
        tree[key] = value

    for key in tree.bfs():
        print(key)

    print()

    for key in tree.dfs():
        print(key)

