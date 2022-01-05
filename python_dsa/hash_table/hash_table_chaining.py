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

