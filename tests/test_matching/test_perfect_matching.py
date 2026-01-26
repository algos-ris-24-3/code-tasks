import unittest
from matching.bipartite_graph import BipartiteGraph
from matching.errors.perfect_matching_error import PerfectMatchingError
from matching.perfect_matching import get_perfect_matching


class TestGetPerfectMatching(unittest.TestCase):

    def test_empty_graph_returns_empty_matching(self):
        """Проверяет, что для пустого графа возвращается пустое совершенное паросочетание."""
        graph = BipartiteGraph({})
        matching = get_perfect_matching(graph)
        self.assertEqual(matching.order, 0)
        self.assertTrue(matching.is_perfect)

    def test_trivial_graph_with_one_edge_returns_perfect_matching(self):
        """Проверяет корректное нахождение совершенного паросочетания в графе порядка 1."""
        graph = BipartiteGraph({0: [0]})
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.get_matching(), [(0, 0)])

    def test_simple_2x2_graph_with_perfect_matching(self):
        """Проверяет нахождение совершенного паросочетания в графе 2x2."""
        graph = BipartiteGraph({0: [0, 1], 1: [0, 1]})
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.cardinality, 2)

    def test_graph_with_unique_perfect_matching(self):
        """Проверяет, что алгоритм находит единственное возможное совершенное паросочетание."""
        graph = BipartiteGraph({
            0: [0],
            1: [1],
            2: [2]
        })
        matching = get_perfect_matching(graph)
        expected = {(0, 0), (1, 1), (2, 2)}
        self.assertEqual(set(matching.get_matching()), expected)

    def test_graph_without_perfect_matching_raises_value_error(self):
        """Проверяет, что при отсутствии совершенного паросочетания выбрасывается ValueError."""
        graph = BipartiteGraph({
            0: [0],
            1: [0],
            2: [0]
        })
        with self.assertRaises(PerfectMatchingError) as cm:
            get_perfect_matching(graph)
        self.assertIn("Совершенное паросочетание не найдено", str(cm.exception))

    def test_graph_with_multiple_perfect_matchings_returns_one_valid(self):
        """Проверяет, что в графе с несколькими совершенными паросочетаниями возвращается корректное."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [0, 1]
        })
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        edges = matching.get_matching()
        self.assertEqual(len(edges), 2)

    def test_graph_4_wo_perfect_matching(self):
        """Проверяет работу алгоритма на графе порядка 4 без совершенного паросочетания."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [1],
            2: [0, 1],
            3: [2, 3],
        })
        with self.assertRaises(PerfectMatchingError):
            get_perfect_matching(graph)

    def test_graph_4_with_perfect_matching(self):
        """Проверяет работу алгоритма на графе порядка 4."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [1],
            2: [0, 1, 2],
            3: [2, 3],
        })
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.cardinality, 4)

    def test_full_graph_with_perfect_matching(self):
        """Проверяет работу алгоритма на полном графе порядка 5."""
        graph = BipartiteGraph({
            i: list(range(5)) for i in range(5)
        })
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.cardinality, 5)

    def test_graph_5_with_perfect_matching(self):
        """Проверяет работу алгоритма на графе порядка 5."""
        graph = BipartiteGraph({
            0: [0, 1],
            1: [0, 4],
            2: [1, 2, 3],
            3: [1, 2, 4],
            4: [0, 4],
        })
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.cardinality, 5)

    def test_graph_5_wo_perfect_matching(self):
        """Проверяет работу алгоритма на графе порядка 5 без совершенного паросочетания."""
        graph = BipartiteGraph({
            0: [0],
            1: [0, 4],
            2: [1, 2, 3],
            3: [1, 2, 4],
            4: [0, 4],
        })
        with self.assertRaises(PerfectMatchingError):
            get_perfect_matching(graph)

    def test_disconnected_vertex_in_left_partition_raises_error(self):
        """Проверяет, что изолированная вершина в левой доле приводит к ошибке."""
        graph = BipartiteGraph({
            0: [],
            1: [0]
        })
        with self.assertRaises(PerfectMatchingError):
            get_perfect_matching(graph)

    def test_graph_10_with_perfect_matching(self):
        """Проверяет работу алгоритма на графе порядка 10."""
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
        matching = get_perfect_matching(graph)
        self.assertTrue(matching.is_perfect)
        self.assertEqual(matching.cardinality, 10)

if __name__ == "__main__":
    unittest.main()
