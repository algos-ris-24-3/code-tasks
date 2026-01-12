from unittest import TestLoader, TestSuite, TextTestRunner

from tests.data_structures.lists.test_doubly_linked_list import TestDoublyLinkedList


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestDoublyLinkedList))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())
