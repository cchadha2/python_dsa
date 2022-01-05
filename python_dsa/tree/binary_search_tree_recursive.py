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
    """Binary Search Tree traditional recursive implementation."""

    def __init__(self):
        self._root = None
        self._size = 0
        self._keys = set()

    def __getitem__(self, key):
        """Get value for given key."""
        node, _ = self._get(key)

        if not node:
            raise KeyError("Given key not in tree")

        return node

    def __setitem__(self, key, value):
        """Set value at given key."""
        self._put(key, value)

    def __delitem__(self, key):
        """Delete item at given key"""
        self._delete(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        return self.in_order() 

    def __contains__(self, key):
        return key in self._keys

    def __repr__(self):
        return f"BinarySearchTree(root={self._root})"

    @property
    def min(self):
        minimum, _ = self._check_extreme(self._root, "left")
        return minimum.key

    @property
    def max(self):
        maximum, _ = self._check_extreme(self._root, "right")
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
        return self._delete_extreme("left")

    def delete_max(self):
        """Delete maximum node in tree."""
        return self._delete_extreme("right")

    def keys(self, minimum=None, maximum=None):
        """Find keys between minimum and maximum keys (inclusive).

        This is a recursive method unfortunately :(
        """
        if minimum is None and maximum is None:
            # TODO: Revert this change after debugging.
            return list(self._keys)
            #return iter(self) 
        #elif (minimum is not None and maximum is None) or (minimum is None and maximum is not None):
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

    def _get(self, key):
        """Get node for given key."""

        def find_node(node, parent=None):
            if not node:
                return node, parent

            if node > key:
                return find_node(node.left, node)
            elif node < key:
                return find_node(node.right, node)

            return node, parent

        return find_node(self._root)

    def _put(self, key, value):
        """Put value at given key."""

        node, parent = self._get(key)
        if not node:
            if not parent:
                self._root = _Node(key, value)
            elif key > parent:
                parent.right = _Node(key, value)
            else:
                parent.left = _Node(key, value)

            self._size += 1
            self._keys.add(key)
        else:
            node.value = value
        
    def _delete(self, key):
        """Delete node at given key."""
        node, parent = self._get(key)
        
        if not node:
            raise KeyError("Given key not in tree")

        if self._size == 1:
            self.delete_min()
            return

        if node.left:
            # Find the predecessor to the node.
            # TODO: Predecessor and successor's children not being moved to replace_parent
            # correctly.
            replace_node, replace_parent = self._check_extreme(node.left, "right", node)
        elif node.right:
            # If there is no predecessor, the replacement node is the successor.
            replace_node, replace_parent = self._check_extreme(node.right, "left", node)
        else:
            replace_node = None


        if not replace_node:
            # There is no predecessor or successor.
            if parent.left is node:
                parent.left = None
            else:
                parent.right = None

        else:
            # Remove the pointer to replacement node on its previous parent.
            if replace_parent:
                if replace_parent.left is replace_node:
                    replace_parent.left = None
                else:
                    replace_parent.right = None
            
            # Update replacement node's children to current node's children.
            replace_node.left, replace_node.right = node.left, node.right

            # If the deleted node was the root, update the _root attribute.
            if not parent:
                self._root = replace_node
            # Otherwise, update the deleted node's parent.
            else:
                if parent.left is node:
                    parent.left = replace_node
                else:
                    parent.right = replace_node

        self._size -= 1
        self._keys.remove(key)

        
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

    def _delete_extreme(self, direction):
        """Delete minimum node in tree."""
        if self._size <= 0:
            raise KeyError("No nodes in tree")
        elif self._size == 1:
            extreme = self._root
            self._root = None
        else:            
            extreme, extreme_parent = self._check_extreme(self._root, direction)

            if not extreme_parent:
                self._root = extreme.left or extreme.right
            elif extreme_parent.left is extreme:
                extreme_parent.left = None
            else:
                extreme_parent.right = None

        self._size -= 1
        self._keys.remove(extreme.key)
        return extreme.key

    def _check_extreme(self, node, direction, parent=None):
        """Find min or max node in tree"""

        def traverse(node, parent, direction):
            if not node:
                return (node, parent)

            extreme_node, extreme_parent = traverse(getattr(node, direction), node, direction)
            return (extreme_node, extreme_parent) if extreme_node else (node, parent)

        return traverse(node, parent, direction)


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
    print(len(tree))
    print(*tree)
    print("a" in tree)
    try:
        print(tree.delete_max())
    except KeyError:
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

    print(tree)
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

