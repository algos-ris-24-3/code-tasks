import unittest
from matching.bipartite_graph_matching import BipartiteGraphMatching


class TestBipartiteGraphMatching(unittest.TestCase):

    def test_init_with_zero_order_creates_empty_matching(self):
        """Проверяет инициализацию паросочетания нулевого порядка."""
        matching = BipartiteGraphMatching(0)
        self.assertEqual(matching.order, 0)
        self.assertEqual(matching.cardinality, 0)

    def test_init_with_positive_order_creates_empty_matching(self):
        """Проверяет инициализацию паросочетания положительного порядка."""
        matching = BipartiteGraphMatching(5)
        self.assertEqual(matching.order, 5)
        self.assertEqual(matching.cardinality, 0)
        for i in range(5):
            self.assertFalse(matching.is_left_covered(i))
            self.assertFalse(matching.is_right_covered(i))

    def test_init_with_negative_order_raises_value_error(self):
        """Проверяет, что инициализация с отрицательным порядком вызывает ValueError."""
        with self.assertRaises(ValueError):
            BipartiteGraphMatching(-1)

    def test_add_edge_with_valid_free_vertices_increases_cardinality(self):
        """Проверяет добавление ребра между свободными вершинами увеличивает мощность."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(0, 1)
        self.assertEqual(matching.cardinality, 1)
        self.assertTrue(matching.is_left_covered(0))
        self.assertTrue(matching.is_right_covered(1))
        self.assertEqual(matching.get_matching(), [(0, 1)])

    def test_add_edge_to_covered_left_vertex_raises_value_error(self):
        """Проверяет, что добавление ребра к уже покрытой левой вершине вызывает ошибку."""
        matching = BipartiteGraphMatching(2)
        matching.add_edge(0, 0)
        with self.assertRaises(ValueError):
            matching.add_edge(0, 1)

    def test_add_edge_to_covered_right_vertex_raises_value_error(self):
        """Проверяет, что добавление ребра к уже покрытой правой вершине вызывает ошибку."""
        matching = BipartiteGraphMatching(2)
        matching.add_edge(0, 0)
        with self.assertRaises(ValueError):
            matching.add_edge(1, 0)

    def test_add_edge_with_out_of_range_left_index_raises_index_error(self):
        """Проверяет, что добавление ребра с недопустимым индексом левой вершины вызывает IndexError."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.add_edge(2, 0)

    def test_add_edge_with_out_of_range_right_index_raises_index_error(self):
        """Проверяет, что добавление ребра с недопустимым индексом правой вершины вызывает IndexError."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.add_edge(0, 2)

    def test_remove_edge_removes_existing_edge_and_decreases_cardinality(self):
        """Проверяет корректное удаление существующего ребра из паросочетания."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(1, 2)
        matching.remove_edge(1, 2)
        self.assertEqual(matching.cardinality, 0)
        self.assertFalse(matching.is_left_covered(1))
        self.assertFalse(matching.is_right_covered(2))
        self.assertEqual(matching.get_matching(), [])

    def test_remove_nonexistent_edge_raises_value_error(self):
        """Проверяет, что удаление несуществующего ребра вызывает ValueError."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(ValueError):
            matching.remove_edge(0, 1)

    def test_remove_edge_with_out_of_range_left_index_raises_index_error(self):
        """Проверяет, что удаление ребра с недопустимым индексом левой вершины вызывает IndexError."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.remove_edge(2, 0)

    def test_remove_edge_with_out_of_range_right_index_raises_index_error(self):
        """Проверяет, что удаление ребра с недопустимым индексом правой вершины вызывает IndexError."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.remove_edge(0, 2)

    def test_get_matching_returns_correct_list_of_edges(self):
        """Проверяет, что get_matching возвращает корректный список рёбер."""
        matching = BipartiteGraphMatching(4)
        matching.add_edge(0, 3)
        matching.add_edge(2, 1)
        expected = [(0, 3), (2, 1)]
        self.assertEqual(sorted(matching.get_matching()), sorted(expected))

    def test_is_perfect_returns_true_when_all_vertices_covered(self):
        """Проверяет, что is_perfect возвращает True для совершенного паросочетания."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(0, 1)
        matching.add_edge(1, 0)
        matching.add_edge(2, 2)
        self.assertTrue(matching.is_perfect)

    def test_is_perfect_returns_false_when_not_all_vertices_covered(self):
        """Проверяет, что is_perfect возвращает False, если не все вершины покрыты."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(0, 1)
        self.assertFalse(matching.is_perfect)

    def test_is_perfect_returns_true_for_zero_order(self):
        """Проверяет, что is_perfect возвращает True для графа нулевого порядка."""
        matching = BipartiteGraphMatching(0)
        self.assertTrue(matching.is_perfect)

    def test_repr_returns_correct_string_representation(self):
        """Проверяет корректность строкового представления объекта."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(0, 2)
        expected = "BipartiteGraphMatching(order=3, matching=[(0, 2)])"
        self.assertEqual(repr(matching), expected)

    def test_get_right_match_returns_correct_value_for_covered_vertex(self):
        """Проверяет, что get_right_match возвращает правильный индекс для покрытой левой вершины."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(1, 2)
        self.assertEqual(matching.get_right_match(1), 2)

    def test_get_right_match_returns_minus_one_for_uncovered_vertex(self):
        """Проверяет, что get_right_match возвращает -1 для непокрытой левой вершины."""
        matching = BipartiteGraphMatching(3)
        self.assertEqual(matching.get_right_match(0), -1)

    def test_get_right_match_raises_index_error_for_out_of_range_index(self):
        """Проверяет, что get_right_match вызывает IndexError при недопустимом индексе левой вершины."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.get_right_match(2)

    def test_get_left_match_returns_correct_value_for_covered_vertex(self):
        """Проверяет, что get_left_match возвращает правильный индекс для покрытой правой вершины."""
        matching = BipartiteGraphMatching(3)
        matching.add_edge(1, 2)
        self.assertEqual(matching.get_left_match(2), 1)

    def test_get_left_match_returns_minus_one_for_uncovered_vertex(self):
        """Проверяет, что get_left_match возвращает -1 для непокрытой правой вершины."""
        matching = BipartiteGraphMatching(3)
        self.assertEqual(matching.get_left_match(0), -1)

    def test_get_left_match_raises_index_error_for_out_of_range_index(self):
        """Проверяет, что get_left_match вызывает IndexError при недопустимом индексе правой вершины."""
        matching = BipartiteGraphMatching(2)
        with self.assertRaises(IndexError):
            matching.get_left_match(2)

if __name__ == "__main__":
    unittest.main()
