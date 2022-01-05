# Rabin-Karp with Binary Search on string to find repeating substrings.

def longestRepeatingSubstring(self, s: str) -> int:

    def check_duplicates(length):
        """Rabin-Karp"""

        h = 0
        for idx, char in enumerate(s[:length]):
            h += ord(char) * (26 ** (length - 1 - idx))

        hashes = set()
        hashes.add(h)

        start, end = 0, length
        while end < len(s):
            h = (h * 26) - (ord(s[start]) * (26 ** length)) + ord(s[end])
            if h in hashes:
                return True
            else:
                hashes.add(h)

            start += 1
            end += 1

        return False

    # Binary search to find length of repeating substrings.
    left, right = 0, len(s) - 1

    while left <= right:
        mid = (left + right) // 2

        if check_duplicates(mid + 1):
            left = mid + 1
        else:
            right = mid - 1

    return left

