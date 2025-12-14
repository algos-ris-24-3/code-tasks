from unittest import TestLoader, TestSuite, TextTestRunner

from tests.problems.knapsack_problem.test_dynamic import TestDynamicSolver


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestDynamicSolver))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
