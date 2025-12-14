import unittest

from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from tests.problems.knapsack_problem.test_abstract import TestAbstractSolver


class TestBruteForceSolver(unittest.TestCase, TestAbstractSolver):
    """Набор тестов для проверки решения задачи о рюкзаке методом полного
    перебора."""

    solver = BruteForceSolver


if __name__ == "__main__":
    unittest.main()
