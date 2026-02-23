from unittest import TestLoader, TestSuite, TextTestRunner

from tests.network_flow.test_max_flow import TestMaxFlow
from tests.network_flow.test_min_cost_flow import TestMinCostFlow
from tests.shortest_path.test_bellman_ford import TestBellmanFord
from tests.shortest_path.test_floyd_warshall import TestFloydWarshall



def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestMaxFlow))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestMinCostFlow))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBellmanFord))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestFloydWarshall))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())