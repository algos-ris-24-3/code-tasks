from unittest import TestLoader, TestSuite, TextTestRunner

from tests.problems.sorting_problem.test_some_sort import TestSomeSort


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestSomeSort))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
