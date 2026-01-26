from unittest import TestLoader, TestSuite, TextTestRunner

from tests.test_matching.test_bipartite_graph import TestBipartiteGraph
from tests.test_matching.test_bipartite_graph_matching import TestBipartiteGraphMatching
from tests.test_matching.test_max_matching import TestMaxMatching


def suite():
    """Создает набор тест-кейсов для тестирования."""
    test_suite = TestSuite()
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBipartiteGraphMatching))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestBipartiteGraph))
    test_suite.addTest(TestLoader().loadTestsFromTestCase(TestMaxMatching))

    return test_suite


if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)
    runner.run(suite())