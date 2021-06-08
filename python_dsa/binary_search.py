# Binary search implementation (assuming pre-sorted subscriptable sequence)
import bisect


def binary_search(seq, elem):
    """Return index of elem in seq."""
    idx = bisect.bisect_left(seq, elem)
    if idx != len(seq) and seq[idx] == elem:
        return idx
    raise ValueError("Value not in sequence")


# Not recommended for use :)
def iterative_binary_search(seq, elem):
    lo, hi = 0, len(seq)
    while lo < hi:
        idx = (hi + lo) // 2
        if seq[idx] < elem:
            lo = idx + 1
        elif seq[idx] > elem:
            hi = idx
        else:
            return idx

    # Return -1 instead of raising ValueError for testing.
    return -1


def recursive_binary_search(seq, elem, lo, hi):
    # print(lo, hi)
    if lo >= hi:
        return -1

    idx = (hi + lo) // 2
    if seq[idx] < elem:
        return recursive_binary_search(seq, elem, lo=idx + 1, hi=hi)
    elif seq[idx] > elem:
        return recursive_binary_search(seq, elem, lo=lo, hi=idx)
    else:
        return idx


if __name__ == "__main__":
    arr = list(range(10))
    print(arr)
    print(arr[bisect.bisect_left(arr, 4)])
    print(arr[bisect.bisect_left(arr, -4)])
    try:
        print(arr[bisect.bisect_left(arr, 15)])
    except IndexError:
        print("Error raised")
    print(arr[bisect.bisect_left(arr, 4.7)])
    print(arr[bisect.bisect_left(arr, 4.2)])
    print(arr[bisect.bisect_left(arr, 2.7)])

    print(arr[bisect.bisect(arr, 5)])
    print(arr[bisect.bisect(arr, -5)])
    print(arr[bisect.bisect(arr, 5.5)])
    try:
        print(arr[bisect.bisect(arr, 15)])
    except IndexError:
        print("Error raised")


    arr = [1, 4, 6, 10, 15, 53]
    print(binary_search(arr, 4))

    print("Starting iterative search")
    print(iterative_binary_search(arr, 6))
    print(iterative_binary_search(arr, 15))
    print(iterative_binary_search(arr, 1))
    print(iterative_binary_search(arr, -5))
    print(iterative_binary_search(arr, 100))
    print(iterative_binary_search(arr, 53))
    print(iterative_binary_search(arr, 54))

    print("Starting recursive search")
    print(recursive_binary_search(arr, 6, 0, len(arr)))
    print(recursive_binary_search(arr, 15, 0, len(arr)))
    print(recursive_binary_search(arr, 1, 0, len(arr)))
    print(recursive_binary_search(arr, -5, 0, len(arr)))
    print(recursive_binary_search(arr, 100, 0, len(arr)))
    print(recursive_binary_search(arr, 53, 0, len(arr)))
    print(recursive_binary_search(arr, 54, 0, len(arr)))

