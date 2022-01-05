from python_dsa.sorting import quick_sort

import unittest


class TestQuickSort(unittest.TestCase):

    def test_small(self):
        arr = [4, 1, 2, 5, 6, 7]
        self.assertEqual(quick_sort(arr), [1, 2, 4, 5, 6, 7])

    def test_duplicates(self):
        arr = [4, 1, 7, 2, 5, 5, 5, 6, 7]
        self.assertEqual(quick_sort(arr), [1, 2, 4, 5, 5, 5, 6, 7, 7])

    def test_empty(self):
        self.assertEqual(quick_sort([]), [])

    def test_one_elem(self):
        self.assertEqual(quick_sort([1]), [1])

    def test_cutoff(self):
        self.assertEqual(quick_sort([4, 1, 2, 5, 6, 7], cutoff=6), [1, 2, 4, 5, 6, 7])


if __name__ == "__main__":
    unittest.main()

