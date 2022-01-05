import heapq
import math
import random
from timeit import repeat

random.seed(77)


# O(n**2). O(1) space. Not stable.
def selection_sort(seq):
    """For each index in seq, swap with minimum value from the remaining values."""
    for idx, elem in enumerate(seq):
        minimum = math.inf
        for other_idx, other_elem in enumerate(seq[idx:], start=idx):
            if minimum > other_elem:
                minimum = other_elem
                min_idx = other_idx
        if minimum != math.inf:
            # Swap elements.
            seq[idx], seq[min_idx] = minimum, elem
    return seq


# O(n**2). O(1) space. Stable sort.
def insertion_sort(seq):
    """For each element, compare and swap with elements to the left."""
    for idx, elem in enumerate(seq):
        other_idx = idx - 1
        while other_idx >= 0:
            other_elem = seq[other_idx]
            if other_elem < elem:
                break

            seq[other_idx + 1] = other_elem
            other_idx -= 1

        if elem < seq[other_idx + 1]:
            seq[other_idx + 1] = elem

    return seq


# O(n**3/2) or thereabouts. Not necessarily quadratic. Not stable.
def shell_sort(seq):
    """Initalize h as a steadily large value, h-sort, and steadily decrease h to completely sort."""
    h = 1
     # 1, 4, 13, 40, 121, 364, 1093, ...
    while h < len(seq) / 3:
        h = 3*h + 1

    while h >= 1:
        for idx in range(h, len(seq)):
            other_idx = idx
            while other_idx >= h and seq[other_idx] < seq[other_idx - h]:
                seq[other_idx], seq[other_idx - h] = seq[other_idx - h], seq[other_idx]
                other_idx -= h
        h //= 3

    return seq


# O(nlogn) guaranteed worst case and O(n) space for auxiliary array.
def merge_sort(seq, cutoff=0):
    """Cut off to insertion sort when seq contains less than or equal to specified number of elements."""
    aux = [None] * len(seq)

    def sort(seq, lo, hi):
        """Recursively split seq into two subarrays and sort (stable)."""
        if hi <= lo:
            return

        if hi - lo <= cutoff:
            seq[lo : hi + 1] = insertion_sort(seq[lo : hi + 1])
        else:
            mid = (hi + lo) // 2
            sort(seq, lo=lo, hi=mid)
            sort(seq, lo=mid + 1, hi=hi)
            merge(seq, lo, mid, hi)

    def merge(seq, lo, mid, hi):
        """Merge subarrays using auxiliary array to find minimum value at each index."""
        first_seq_start, second_seq_start = lo, mid + 1

        aux[lo : hi + 1] = seq[lo : hi + 1]
        for idx in range(lo, hi + 1):
            if first_seq_start > mid:
                seq[idx] = aux[second_seq_start]
                second_seq_start += 1

            elif second_seq_start > hi:
                seq[idx] = aux[first_seq_start]
                first_seq_start += 1
            elif aux[second_seq_start] < aux[first_seq_start]:
               seq[idx] = aux[second_seq_start]
               second_seq_start += 1
            else:
                seq[idx] = aux[first_seq_start]
                first_seq_start += 1

    sort(seq, lo=0, hi=len(seq) - 1)
    return seq


# O(nlogn) average case. Generally faster than mergesort due to less data movement. O(n**2) at worst.
# Between O(logn) and O(n) space complexity due to recursive sort calls.
def quick_sort(seq, cutoff=0):
    """Scan seq from both left and right (converging in center) and sort by exchanging values."""
    # Shuffle seq to avoid worst case time complexity of O(n**2).
    random.shuffle(seq)

    def sort(seq, lo, hi):
        """Recursively sort subarrays of seq split on partition value."""
        if hi <= lo:
            return

        if hi - lo <= cutoff:
            seq[lo : hi + 1] = insertion_sort(seq[lo : hi + 1])
        else:
            idx = partition(seq, lo, hi)
            sort(seq, lo, idx - 1)
            sort(seq, idx + 1, hi)

    def partition(seq, lo, hi):
        """Find partition index which is in correct sorted place."""
        from_left, from_right = lo, hi
        partition_value = seq[lo]
        while True:
            # Find leftmost value from partition that is greater than partition.
            from_left += 1
            while seq[from_left] < partition_value:
                if from_left == hi:
                    break
                from_left += 1

            # Find rightmost value from other side that is less than partition.
            while seq[from_right] > partition_value:
                if from_right == lo:
                    break
                from_right -= 1

            if from_left >= from_right:
                break
            # Exchange left and right values.
            seq[from_left], seq[from_right] = seq[from_right], seq[from_left]

        # Exchange parition with left-most value (which is now from_right).
        seq[lo], seq[from_right] = seq[from_right], seq[lo]

        return from_right

    sort(seq, 0, len(seq) - 1)
    return seq


# O(n) best case with equal keys. O(n**2) worst case and O(nlogn) average case (same as quicksort).
# Uses O(logn) space for recursion.
def three_way_quick_sort(seq, cutoff=0):
    """Quicksort variation used to quickly sort sequences with duplicate elements"""
    # Shuffle seq to avoid worst case time complexity of O(n**2).
    random.shuffle(seq)

    def sort(seq, lo, hi):
        """Puts keys equal to the partitioning element together in sorted order."""
        if hi < lo:
            return

        if hi - lo <= cutoff:
            seq[lo : hi + 1] = insertion_sort(seq[lo : hi + 1])
        else:
            partition_value = seq[lo]
            partition_idx, idx, from_right = lo, lo + 1, hi
            while idx <= from_right:
                # Swap partition value with current index value if it is less than current index
                # value. Then move the partition value pointer up one to match the swap.
                if seq[idx] < partition_value:
                    seq[partition_idx], seq[idx] = seq[idx], seq[partition_idx]
                    partition_idx += 1
                    idx += 1
                # Otherwise, if the current index value is greater than the partition value, swap
                # the current index value with the value in the index from_right. This brings any of
                # the large values on the right hand side of the sequence to the left.
                elif seq[idx] > partition_value:
                    seq[from_right], seq[idx] = seq[idx], seq[from_right]
                    from_right -= 1
                # If the paritition value is equal to the current index value, advance to the next
                # index.
                else:
                    idx += 1

            # Partition index and from_right are the bounds of one value's indices. Repeat the sort
            # for other values.
            sort(seq, lo, partition_idx - 1)
            sort(seq, from_right + 1, hi)

    sort(seq, 0, len(seq) - 1)
    return seq


def heap_sort(seq):
    """Constructs a heap and iterates over each element to sink it to correct positon"""
    def sink(value, length):
        while 2 * value <= length:
            next_node = 2 * value
            if next_node < length and seq[next_node] < seq[next_node + 1]:
                next_node += 1
            if not seq[value] < seq[next_node]:
                break
            seq[value], seq[next_node] = seq[next_node], seq[value]
            value = next_node

    # Construct the heap.
    for value in range(len(seq) // 2, -1, -1):
        sink(value, len(seq) - 1)

    # Sort the elements by sinking each node to its correct position.
    n = len(seq) - 1
    while n > 0:
        # Exchange bottom node with largest (root) node.
        seq[0], seq[n] = seq[n], seq[0]
        n -= 1
        # Sink the new root node to its correct position while removing the exchanged root node from
        # the sink (by above decrement of n).
        sink(0, n)

    return seq

def heapq_sort(seq):
    """Heap sort implementation using heapq module."""
    heapq.heapify(seq)
    return [heapq.heappop(seq) for _ in range(len(seq))]

def main(seq):
    """Runs each sort on seq"""
    # Sort individually ahead of time to check correctness.
    system_sort = sorted(seq)
    selection = selection_sort(seq.copy())
    insertion = insertion_sort(seq.copy())
    shell = shell_sort(seq.copy())
    merge = merge_sort(seq.copy())
    quick = quick_sort(seq.copy())
    heap = heap_sort(seq.copy())
    heapq_result = heapq_sort(seq.copy())

    # Improved sorts.
    cutoff = 10
    merge_with_cutoff = merge_sort(seq.copy(), cutoff)
    quick_with_cutoff = quick_sort(seq.copy(), cutoff)
    three_way_quick = three_way_quick_sort(seq.copy())
    three_way_quick_with_cutoff = three_way_quick_sort(seq.copy(), cutoff)

    num_times = 10
    rep = 1

    def min_time(sort_type, **kwargs):
        stmt = ((f"{sort_type}({seq.copy()}, "
                f"{', '.join('='.join((str(k), str(v))) for k, v in kwargs.items())})")
                if kwargs else f"{sort_type}({seq.copy()})")

        if sort_type != "sorted":
            times = repeat(setup=f'from __main__ import {sort_type}',
                           stmt=stmt,
                           repeat=rep, number=num_times)
        else:
            times = repeat(stmt=f"sorted({seq.copy()})", repeat=rep, number=num_times)
        return min(times)

    print(f"Call sorting function {num_times} time(s) and repeat {rep} time(s) each for a total of "
          f"{num_times * rep} calls")
    print("Type of sort: Sorted or not: Min time (seconds)")
    print(f"Unsorted seq: {seq == system_sort}, number of elements: {len(seq)}")
    print(f"System sort: True : {min_time('sorted')}")
    print(f"Selection sort: {selection == system_sort} : {min_time('selection_sort')}")
    print(f"Insertion sort: {insertion == system_sort} : {min_time('insertion_sort')}")
    print(f"Shell sort: {shell == system_sort} : {min_time('shell_sort')}")
    print(f"Merge sort: {merge == system_sort} : {min_time('merge_sort')}")
    print(f"Merge sort with cutoff: {merge_with_cutoff == system_sort} : {min_time('merge_sort', cutoff=cutoff)}")
    print(f"Quick sort: {quick == system_sort} : {min_time('quick_sort')}")
    print(f"Quick sort with cutoff: {quick_with_cutoff == system_sort} : {min_time('quick_sort', cutoff=cutoff)}")
    print(f"Three way quick sort: {three_way_quick == system_sort} : {min_time('three_way_quick_sort')}")
    print(f"Three way quick sort with cutoff: {three_way_quick_with_cutoff == system_sort} :"
          f"{min_time('three_way_quick_sort', cutoff=cutoff)}")
    print(f"Heap sort: {heap == system_sort} : {min_time('heap_sort')}")
    print(f"Heap with heapq sort: {heapq_result == system_sort} : {min_time('heapq_sort')}", end="\n\n")

if __name__ == "__main__":
    print("Random array")
    main([random.randint(0, 10**4) for _ in range(5)])
    print("Random array")
    main([random.randint(0, 10**3) for _ in range(50)])
    print("Random array with duplicates")
    main([random.randint(0, 50) for _ in range(500)])
    print("Sorted array")
    main([elem for elem in range(500)])
    print("Random array")
    main([random.randint(0, 10**8) for _ in range(5000)])
    print("Random array with duplicates")
    main([random.randint(0, 50) for _ in range(5000)])
    print("Reverse array")
    main([elem for elem in range(5000, 0, -1)])
    print("Random array")
    main([random.randint(0, 10**20) for _ in range(10000)])
    print("Reverse array")
    main([elem for elem in range(10000, 0, -1)])
