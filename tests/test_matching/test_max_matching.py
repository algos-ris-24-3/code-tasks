import unittest
from matching.bipartite_graph import BipartiteGraph
from matching.max_matching import get_max_matching


class TestMaxMatching(unittest.TestCase):

    def test_empty_graph_returns_empty_matching(self):
        """Проверяет, что для пустого графа возвращается пустое паросочетание."""
        graph = BipartiteGraph({})
        matching = get_max_matching(graph)
        self.assertEqual(matching.order, 0)
        self.assertEqual(matching.cardinality, 0)

    def test_single_vertex_with_no_edges_returns_empty_matching(self):
        """Проверяет, что изолированная вершина даёт пустое паросочетание."""
        graph = BipartiteGraph({0: []})
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 0)
        self.assertFalse(matching.is_perfect)

    def test_trivial_graph_with_one_edge_returns_matching_of_size_one(self):
        """Проверяет нахождение максимального паросочетания в графе порядка 1 с ребром."""
        graph = BipartiteGraph({0: [0]})
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 1)
        self.assertTrue(matching.is_perfect)

    def test_simple_2x2_complete_graph_returns_matching_of_size_two(self):
        """Проверяет, что в полном графе 2x2 находится паросочетание мощности 2."""
        graph = BipartiteGraph({0: [0, 1], 1: [0, 1]})
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 2)
        self.assertTrue(matching.is_perfect)

    def test_graph_with_unique_perfect_matching_finds_it(self):
        """Проверяет, что уникальное совершенное паросочетание находится корректно."""
        graph = BipartiteGraph({
            0: [0],
            1: [1],
            2: [2]
        })
        matching = get_max_matching(graph)
        expected = {(0, 0), (1, 1), (2, 2)}
        self.assertEqual(set(matching.get_matching()), expected)
        self.assertTrue(matching.is_perfect)

    def test_graph_without_perfect_matching_returns_maximal_non_perfect(self):
        """Проверяет, что в графе без совершенного паросочетания возвращается максимальное неполное."""
        graph = BipartiteGraph({
            0: [0],
            1: [0],
            2: [0]
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 1)
        self.assertFalse(matching.is_perfect)

    def test_graph_with_multiple_perfect_matchings_returns_one_valid(self):
        """Проверяет, что в графе с несколькими совершенными паросочетаниями возвращается корректное."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [0, 1]
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 2)
        self.assertTrue(matching.is_perfect)

    def test_graph_4_without_perfect_matching_returns_maximal_matching(self):
        """Проверяет максимальное паросочетание в графе порядка 4 без совершенного."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [1],
            2: [0, 1],
            3: [2, 3],
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 3)
        self.assertFalse(matching.is_perfect)

    def test_graph_4_with_perfect_matching_finds_it(self):
        """Проверяет, что совершенное паросочетание в графе порядка 4 находится."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [1],
            2: [0, 1, 2],
            3: [2, 3],
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 4)
        self.assertTrue(matching.is_perfect)

    def test_full_graph_returns_perfect_matching(self):
        """Проверяет, что в полном двудольном графе находится совершенное паросочетание."""
        graph = BipartiteGraph({
            i: list(range(5)) for i in range(5)
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 5)
        self.assertTrue(matching.is_perfect)

    def test_disconnected_vertex_in_left_partition_handled_correctly(self):
        """Проверяет, что изолированная вершина не ломает алгоритм и не включается в паросочетание."""
        graph = BipartiteGraph({
            0: [],
            1: [0]
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 1)
        self.assertFalse(matching.is_perfect)
        self.assertFalse(matching.is_left_covered(0))
        self.assertTrue(matching.is_left_covered(1))

    def test_large_graph_with_perfect_matching_finds_it(self):
        """Проверяет работу алгоритма на графе порядка 10 с совершенным паросочетанием."""
        graph = BipartiteGraph({
            0: [0, 1, 2, 9],
            1: [9],
            2: [1, 3],
            3: [0, 3, 5],
            4: [3, 6],
            5: [3, 7, 8],
            6: [4, 8],
            7: [5, 8],
            8: [7],
            9: [6, 8, 9],
        })
        matching = get_max_matching(graph)
        self.assertEqual(matching.cardinality, 10)
        self.assertTrue(matching.is_perfect)

if __name__ == "__main__":
    unittest.main()
