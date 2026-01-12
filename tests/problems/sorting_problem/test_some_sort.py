import unittest

from problems.sorting_problem.some_sort import some_sort
from tests.problems.sorting_problem.test_abstract import TestAbstractSorter


class TestSomeSort(unittest.TestCase, TestAbstractSorter):
    """Набор тестов для проверки некоторого метода сортировки."""

    sort_method = lambda _, items: some_sort(items)


if __name__ == "__main__":
    unittest.main()
