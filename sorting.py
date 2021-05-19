import math
import random

from handy_decorators import timer

random.seed("My fun sorting module")

# O(n**2). O(1) space. Not stable.
@timer
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
@timer
def insertion_sort(seq):
    """For each element, compare and swap with elements to the left."""
    for idx, elem in enumerate(seq):
        other_idx = idx - 1
        while other_idx >= 0:
            other_elem = seq[other_idx]
            if elem > other_elem:
                break

            # Swap elements.
            seq[idx], seq[other_idx] = other_elem, elem
            other_idx -= 1

    return seq


# O(n**3/2) or thereabouts. Not necessarily quadratic. Not stable.
@timer
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
@timer
def merge_sort(seq):
    aux = [None] * len(seq)

    def sort(seq, lo, hi):
        """Recursively split seq into two subarrays and sort (stable)."""
        if hi <= lo:
            return
        mid = (hi + lo) // 2
        sort(seq, lo=lo, hi=mid)
        sort(seq, lo=mid + 1, hi=hi)
        merge(seq, lo, mid, hi)

    def merge(seq, lo, mid, hi):
        """Merge subarrays using auxiliary array to find minimum value at each index."""
        first_seq_start, second_seq_start = lo, mid + 1

        seq_slice = slice(lo, hi + 1)
        aux[seq_slice] = seq[seq_slice]
        for idx in range(seq_slice.start, seq_slice.stop):
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
@timer
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
@timer
def three_way_quick_sort(seq):
    """Quicksort variation used to quickly sort sequences with duplicate elements"""


def main(seq):
    """Runs each sort on seq"""
    system_sort = sorted(seq)
    print("Sorted?")
    print(f"Unsorted seq: {seq == system_sort}")
    print(f"Selection sort: {selection_sort(seq) == system_sort}")
    print(f"Insertion sort: {insertion_sort(seq) == system_sort}")
    print(f"Shell sort: {shell_sort(seq) == system_sort}")
    print(f"Merge sort: {merge_sort(seq) == system_sort}")
    print(f"Quick sort: {quick_sort(seq) == system_sort}", end="\n\n")



if __name__ == "__main__":
    main([4, 3, 1, 5, 6])
    main([8, 2, 6, 3, 1, 5, 7, 8, 44, 1, 3, 344, 5, 7, 2, 3, 9, 1, 2, 3, 4])
    main([random.randint(0, 100000) for _ in range(3000)])
    main([random.randint(0, 100000000) for _ in range(10000)])

