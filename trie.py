# Trie implementation.
class Node:
    def __init__(self, radix, idx=None, value=None):
        self.idx = idx
        self.value = value
        self.children = [None] * radix

    def __repr__(self):
        return (f"{{Value: {self.value}, Index: {self.idx}, "
                f"Children: {list(filter(None, self.children))}}}")


class Trie:
    # Extended ASCII.
    radix = 256

    def __init__(self):
        self._root = Node(self.radix)
        self._size = 0

    def __getitem__(self, key):
        item = self._get(self._root, key, depth=0)
        if not item.value:
            raise KeyError("Key not found")

        return item.value

    def __setitem__(self, key, val):
        self._put(self._root, key, val, depth=0)

    def __delitem__(self, key):
        self._delete(self._root, key, depth=0)

    def __repr__(self):
        return f"Trie(radix={self.radix})"

    def __str__(self):
        return str(self._root)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        else:
            return True

    def __bool__(self):
        return self._size > 0

    def longest_prefix(self, text):
        return self._find_longest_prefix(self._root, text, depth=0, prefix=None)

    def keys(self):
        return self._populate_keys(self._root)

    def keys_with_prefix(self, prefix):
        return self._populate_keys(self._get(self._root, key=prefix, depth=0), prefix)

    def keys_that_match(self, pattern):
        return self._populate_keys(self._root, pattern=pattern)

    def _get(self, node, key, depth):
        idx = ord(key[depth])
        if not node.children[idx]:
            raise KeyError("Key not found")
        if depth == len(key) - 1:
            return node.children[idx]
        else:
            return self._get(node.children[idx], key, depth + 1)

    def _put(self, node, key, val, depth):
        idx = ord(key[depth])
        if not node.children[idx]:
            node.children[idx] = Node(self.radix, idx)
        if depth == len(key) - 1:
            node.children[idx].value = val
            self._size += 1
            return
        else:
            return self._put(node.children[idx], key, val, depth + 1)

    def _delete(self, node, key, depth):
        idx = ord(key[depth])
        # print(node, chr(idx))
        if not node.children[idx]:
            raise KeyError("Key not found")
        if depth == len(key) - 1:
            if node.children[idx].value:
                if any(node.children[idx].children):
                    node.children[idx].value = None
                    return
                node.children[idx] = None
                return
            return

        self._delete(node.children[idx], key, depth + 1)
        if not node.children[idx].value and not any(node.children[idx].children):
            node.children[idx] = None
            return

    def _find_longest_prefix(self, node, text, depth, prefix):
        idx = ord(text[depth])
        if node.children[idx]:
            if depth == len(text) - 1:
                return prefix
            elif node.children[idx].value is not None:
                prefix = text[:depth + 1]
            return self._find_longest_prefix(node.children[idx], text, depth + 1, prefix)
        return prefix

    def _populate_keys(self, node, prefix="", pattern=""):
        list_of_keys = []
        if not pattern or pattern == ".":
            self._collect_keys(node, list_of_keys, prefix)
        else:
            self._collect_keys_with_pattern(node, list_of_keys, prefix, pattern)
        return list_of_keys

    def _collect_keys(self, node, keys_so_far, prefix):
        for idx, char in enumerate(node.children):
            if not char:
                continue

            next_prefix = prefix + chr(idx)
            if char.value:
                keys_so_far.append(next_prefix)

            self._collect_keys(char, keys_so_far, next_prefix)

        return

    def _collect_keys_with_pattern(self, node, keys_so_far, prefix, pattern):
        next_char = pattern[len(prefix)]
        idx = ord(next_char)
        char = node.children[idx]
        if not char:
            return

        next_prefix = prefix + chr(idx)
        depth = len(next_prefix)
        if depth == len(pattern):
            if char.value:
                keys_so_far.append(next_prefix)
            return

        self._collect_keys_with_pattern(char, keys_so_far, next_prefix, pattern)


if __name__ == "__main__":
    trie = Trie()
    text = "hello"

    print(trie)
    try:
        trie[text]
    except KeyError:
        print("KeyError raised succesfully")

    trie[text] = 5
    print(trie)

    print(len(trie))

    print(trie[text])

    print("hi" in trie)
    print("hello" in trie)

    print(bool(trie))

    print(bool(Trie()))

    trie["he"] = 2

    print(len(trie))
    print(trie)
    print(trie.longest_prefix("hell"))

    trie["helloooooooo my man!!!"] = 54

    print(trie.longest_prefix("hellooooo"))
    print(trie.longest_prefix("goose"))

    for key in ("fly", "help", "woop", "zebra", "zimmy"):
        trie[key] = 999
    print(trie.keys())
    print(trie.keys_with_prefix("hell"))

    print(trie.longest_prefix("zebras are the best huh"))

    print(trie.keys_that_match("."))
    print(trie.keys_that_match("hello"))
    print(trie.keys_that_match("h"))
    print(trie.keys_that_match("hel"))
    print(trie.keys_that_match("fly"))
    print(trie.keys_that_match("zebra"))

    trie = Trie()
    trie["hello"] = 5
    trie["he"] = 2
    trie["help"] = 1
    trie["fly"] = 6
    print(trie, end="\n\n")
    del trie["hello"]
    print(trie)

    trie["hello"] = 5

    del trie["help"]
    print(trie)

    trie["help"] = 1
    del trie["he"]
    print(trie)

    trie["he"] = 2
    del trie["fly"]
    print(trie)
