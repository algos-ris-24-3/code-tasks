import unittest

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from tests.problems.knapsack_problem.test_abstract import TestAbstractSolver



class TestBranchAndBoundSolver(unittest.TestCase, TestAbstractSolver):
    """Набор тестов для проверки решения задачи о рюкзаке методом  ветвей и границ."""

    solver = BranchAndBoundSolver


if __name__ == "__main__":
    unittest.main()
