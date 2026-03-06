from unittest import TestLoader, TestSuite, TextTestRunner

from tests.problems.knapsack_problem.test_bb import TestBranchAndBoundSolver
from tests.problems.knapsack_problem.test_brute_force import TestBruteForceSolver
from tests.problems.knapsack_problem.test_genetic import TestGeneticSolver


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBruteForceSolver))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBranchAndBoundSolver))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestGeneticSolver))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
