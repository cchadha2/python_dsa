# Rabin-Karp with Binary Search on string to find repeating substrings.

def longestRepeatingSubstring(self, s: str) -> int:
    """O(MlogM) time and O(M) space where M is length of string."""

    start = ord("a")
    unique = 26

    # O(M) time where M is length of s. O(M) space at worst for
    # hashset.
    def rabin_karp(length):

        seen = set()

        value = 0
        for idx in range(length):
            value += (ord(s[idx]) - start) * (unique ** idx)

        seen.add(value)

        for idx in range(length, len(s)):
            value -= (ord(s[idx - length]) - start)
            value //= unique
            value += (ord(s[idx]) - start) * (unique ** (length - 1))

            if value in seen:
                return True

            seen.add(value)
        #print(seen, length, s)
        return False


    # O(logM) time binary search over lengths to find
    # largest length repeating substring.
    max_length = 0
    lo, hi = 0, len(s) - 1
    while lo <= hi:
        length = (lo + hi) // 2

        if rabin_karp(length):
            max_length = length
            lo = length + 1
        else:
            hi = length - 1

    return max_length
