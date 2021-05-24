# Separate Chaining and Linear Probing Hash Tables.
from dataclasses import dataclass
from typing import Union


@dataclass
class Item:
    # Immutable builtin types.
    key: Union[int, str, tuple, float, bytes, frozenset]
    value: object


class HashTableSeparateChaining:

    # Sufficiently large to avoid long chains.
    size = 64

    def __init__(self, **pairs):
        self.table = [[] for _ in range(self.size)]

        if pairs:
            for key, value in pairs.items():
                self.put(key, value)

    def hash(self, key):
        return hash(key) % self.size

    def get(self, key):
        idx = self.hash(key)
        for item in self.table[idx]:
            if item.key == key:
                return item.value
        return None

    def put(self, key, value):
        idx = self.hash(key)
        for item in self.table[idx]:
            if item.key == key:
                item.value = value
                return
        self.table[idx].append(Item(key, value))

    def delete(self, key):
        idx = self.hash(key)
        for inner_idx, item in enumerate(self.table[idx]):
            if item.key == key:
                break
        else:
            raise KeyError("Key not found")

        for overwrite_idx, item in enumerate(self.table[idx][inner_idx : -1], start=inner_idx):
            self.table[idx][overwrite_idx] = self.table[idx][overwrite_idx + 1]

        # Get rid of final duplicate value.
        self.table[idx].pop()

    def __getitem__(self, key):
        item = self.get(key)
        if not item:
            raise KeyError("Key not found")

        return item

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.delete(key)


class HashTableLinearProbing:

    def __init__(self, size=8, **pairs):
        # Pre-allocate some space to the hash table.
        self.table = [None] * size
        self.size = size
        self.keys = set()
        self.num_pairs = 0

        if pairs:
            for key, value in pairs.items():
                self.put(key, value)
                print(self.table)

    def hash(self, key):
        # TODO: When size changes, hashed index of put item changes :/
        # Hashed values of strings seem to be changing?
        print(hash(key), hash(key) % self.size)
        return hash(key) % self.size

    def get(self, key):
        idx = self.hash(key)
        for other_idx, remaining_item in enumerate(self.table[idx:], start=idx):
            if remaining_item is None:
                return None
            elif remaining_item.key == key:
                return remaining_item.value

        return None

    def put(self, key, value):
        if self.num_pairs > self.size // 2:
            self._resize(2 * self.size)

        idx = self.hash(key)
        for other_idx, remaining_item in enumerate(self.table[idx:], start=idx):
            if remaining_item is None:
                self.table[other_idx] = Item(key, value)
                self.keys.add(key)
                self.num_pairs += 1
                return
            elif remaining_item.key == key:
                remaining_item.value = value
                return

        self.table.append(Item(key, value))
        self.keys.add(key)
        self.num_pairs += 1

    def delete(self, key):
        """Requires reinsertion of all keys in cluster to the right of the deleted key."""
        idx = self.hash(key)
        item  = self.table[idx]
        # TODO: Finish this method

    def __getitem__(self, key):
        item = self.get(key)
        if not item:
            raise KeyError("Key not found")

        return item

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        raise NotImplementedError

    def _resize(self, new_size):
        new_table = HashTableLinearProbing(size=new_size)
        for key in self.keys:
            new_table[key] = self.get(key)

        self.table = new_table.table
        self.size = new_size

    def __repr__(self):
        return str(self.table)

    def __len__(self):
        return self.num_pairs

if __name__ == "__main__":
    table = HashTableSeparateChaining(hi=1, why=3, a=6)

    print(table['hi'])
    print(table['why'])
    print(table['a'])

    table['new'] = 10
    print(table['new'])

    del table['new']
    del table['a']

    try:
        table['new']
    except KeyError:
        print("Correctly deleted new key")

    try:
        table['a']
    except KeyError:
        print("Correctly deleted 'a' key")

    try:
        table['none']
    except KeyError:
        print("Correctly raised error when getting non-existent key")

    table = HashTableLinearProbing(hi=1, why=3, a=6)

    print(table['hi'])
    print(table.hash("hi"))
    print(table['why'])
    print(table.hash("why"))
    print(table['a'])
    print(table.hash("a"))
    print(table)

    table['new'] = 10
    print(table.hash("new"))
    print(table['new'])

    try:
        table['none']
    except KeyError:
        print("Correctly raised error when getting non-existent key")

    print(table)
    for elem in "hi", "why", "a", "new":
        print(hash(elem), table.hash(elem))
    print(table, table.size)
