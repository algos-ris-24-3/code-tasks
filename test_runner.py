from unittest import TestLoader, TestSuite, TextTestRunner

from tests.data_structures.test_linkedlist import TestLinkedList


def suite():
    """Создает набор тест-кейсов для тестирования модуля для решения задачи
    о рюкзаке."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestLinkedList))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
