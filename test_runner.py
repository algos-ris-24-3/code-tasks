from unittest import TestLoader, TestSuite, TextTestRunner

from tests.test_network_cuts import TestNetworkCuts


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestNetworkCuts))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())