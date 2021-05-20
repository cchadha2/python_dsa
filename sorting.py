import math
import random
from statistics import mean
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
def quick_sort(seq):
    """Scan seq from both left and right (converging in center) and sort by exchanging values."""
    # Shuffle seq to avoid worst case time complexity of O(n**2).
    random.shuffle(seq)

    def sort(seq, lo, hi):
        """Recursively sort subarrays of seq split on partition value."""
        if hi <= lo:
            return
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
def three_way_quick_sort(seq):
    """Quicksort variation used to quickly sort sequences with duplicate elements"""


def main(seq):
    """Runs each sort on seq"""
    # Sort individually ahead of time to check correctness.
    system_sort = sorted(seq)
    selection = selection_sort(seq.copy())
    insertion = insertion_sort(seq.copy())
    shell = shell_sort(seq.copy())
    merge = merge_sort(seq.copy())
    cutoff = 10
    merge_with_cutoff = merge_sort(seq.copy(), cutoff)
    quick = quick_sort(seq.copy())

    num_times = 10
    rep = 1

    def time_stats(sort_type, **kwargs):
        stmt = f"{sort_type}({seq.copy()}, {', '.join('='.join((str(k), str(v))) for k, v in kwargs.items())})" if kwargs else f'{sort_type}({seq.copy()})'
        if sort_type != "sorted":
            times = repeat(setup=f'from __main__ import {sort_type}',
                           stmt=stmt,
                           repeat=rep, number=num_times)
        else:
            times = repeat(stmt=f"sorted({seq.copy()})", repeat=rep, number=num_times)
        return f"Min time {min(times)}"

    print(f"Call sorting function {num_times} time(s) and repeat {rep} time(s) each for a total of "
          f"{num_times * rep} calls")
    print("Type of sort: Sorted or not: Min time")
    print(f"Unsorted seq: {seq == system_sort}, number of elements: {len(seq)}")
    print(f"System sort: True : {time_stats('sorted')}")
    print(f"Selection sort: {selection == system_sort} : {time_stats('selection_sort')}")
    print(f"Insertion sort: {insertion == system_sort} : {time_stats('insertion_sort')}")
    print(f"Shell sort: {shell == system_sort} : {time_stats('shell_sort')}")
    print(f"Merge sort: {merge == system_sort} : {time_stats('merge_sort')}")
    print(f"Merge sort with cutoff: {merge_with_cutoff == system_sort} : {time_stats('merge_sort', cutoff=cutoff)}")
    print(f"Quick sort: {quick == system_sort} : {time_stats('quick_sort')}", end="\n\n")


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
    print("Reverse array")
    main([elem for elem in range(5000, 0, -1)])
    print("Random array")
    main([random.randint(0, 10**20) for _ in range(10000)])
    print("Reverse array")
    main([elem for elem in range(10000, 0, -1)])

