import unittest


from tests.problems.tsp_problem.test_abstract import TestAbstractTspSolver
from problems.tsp_problem.brute_force_tsp_solver import BruteForceTspSolver


class TestTspBruteForceSolver(unittest.TestCase, TestAbstractTspSolver):
    """Набор тестов для проверки решения задачи о рюкзаке методом полного
    перебора."""

    solver = BruteForceTspSolver


if __name__ == "__main__":
    unittest.main()
