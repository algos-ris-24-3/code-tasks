from unittest import TestLoader, TestSuite, TextTestRunner

from problems.tsp_problem.brute_force_tsp_solver import BruteForceTspSolver
from tests.generators.test_permutation_generator import TestPermutationGenerator


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestPermutationGenerator))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(BruteForceTspSolver))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
