# Separate Chaining and Linear Probing Hash Tables.
from dataclasses import dataclass
from typing import Union

from python_dsa.hash_table.hash_table_chaining import Item


class HashTableLinearProbing:

    def __init__(self, size=8, **pairs):
        # Pre-allocate some space to the hash table.
        self.table = [None] * size
        self.initial_size = self.size = size
        self.num_pairs = 0

        if pairs:
            for key, value in pairs.items():
                self.put(key, value)

    def hash(self, key):
        # Python randomly seeds hash values for each process to avoid attackers exploiting
        # predictable hashed values to create collisions in data structures like dicts.
        # This behaviour can be overriden for testing by setting PYTHONHASHSEED env variable.
        # See here for more info:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONHASHSEED
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
        if self.num_pairs >= self.size // 2:
            self._resize(2 * self.size)

        idx = self.hash(key)
        for other_idx, remaining_item in enumerate(self.table[idx:], start=idx):
            if remaining_item is None:
                self.table[other_idx] = Item(key, value)
                self.num_pairs += 1
                return
            elif remaining_item.key == key:
                remaining_item.value = value
                return

        self.table.append(Item(key, value))
        self.num_pairs += 1

    def delete(self, key):
        """Requires reinsertion of all keys in cluster to the right of the deleted key."""
        if not self.__contains__(key):
            return

        idx = self.hash(key)
        while self.table[idx] and key != self.table[idx].key:
            idx = (idx + 1) % self.size

        self.table[idx] = None
        self.num_pairs -= 1

        # Reinsert all keys to the right of the deleted key.
        idx = (idx + 1) % self.size
        while self.table[idx]:
            item, self.table[idx] = self.table[idx], None
            self.num_pairs -= 1

            # This is a little inefficient as it creates a new Item object for each re-insert.
            # Could get around this by separately maintaining keys and values lists into which
            # we simply insert given objects without creating a new custom object to hold the
            # information.
            self.put(item.key, item.value)
            idx = (idx + 1) % self.size

        # Ensure that the load factor (load = num_pairs // size) is not less than or equal to
        # 1 / initial size.
        # If it is, halve the size of the table so that 2 / initial_size >= load factor >= 2 / size.
        # For example, if the size of the table is 16 and there are currently 3 items in the table
        # (before our deletion), then the load factor is 3 / 16 > 1 / 8. Once an item is deleted, we
        # reach a load factor of 2 / 16 = 1 / 8 and so the table is halved to a size of 8 and we
        # have a new load factor of 1 / 4 which is between 1 / initial size and 1 / 2 (optimal
        # performance).
        if self.size // self.initial_size >= self.num_pairs > 0:
            self._resize(self.size // 2)


    def __getitem__(self, key):
        item = self.get(key)
        if not item:
            raise KeyError("Key not found")

        return item

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def _resize(self, new_size):
        new_table = HashTableLinearProbing(size=new_size)
        for item in self.table:
            if item is not None:
                new_table[item.key] = item.value

        self.table = new_table.table
        self.size = new_size

    def __repr__(self):
        return str(self.table)

    def __len__(self):
        return self.num_pairs

    def __contains__(self, key):
        return bool(self.get(key))

if __name__ == "__main__":

    table = HashTableLinearProbing(hi=1, why=3, a=6)

    print(table['hi'])
    print(table.hash("hi"))
    print(table['why'])
    print(table.hash("why"))
    print(table['a'])
    print(table.hash("a"))
    print(table)
    # Should stay between 1/8 and 1/2 for best performance.
    print(f"Load factor of linear probing table = {table.num_pairs / table.size}")

    table['new'] = 10
    table['ye'] = 5
    table['five'] = 21
    print(f"Load factor of linear probing table = {table.num_pairs / table.size}")

    table['fie'] = 21
    table['fve'] = 21
    print(f"Load factor of linear probing table = {table.num_pairs / table.size}")

    table['ive'] = 21
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

    print(f"Load factor of linear probing table = {table.num_pairs / table.size}")

    print(f"Is 'hi' in the table? {'hi' in table}")
    print(f"Is 'woop' in the table? {'woop' in table}")

    print(f"Table before deletion of 'hi' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")
    del table['hi']
    print(f"Table after deletion of 'hi' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")
    del table['why']
    print(f"Table after deletion of 'why' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")
    del table['new']
    print(f"Table after deletion of 'new' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")
    del table['ive']
    print(f"Table after deletion of 'ive' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")
    del table['fie']
    print(f"Table after deletion of 'fie' {table}. Table size: {table.size}. Num items: "
          f"{table.num_pairs}. Load factor: {table.num_pairs / table.size}")

