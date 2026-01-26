import unittest
from matching.bipartite_graph import BipartiteGraph


class TestBipartiteGraph(unittest.TestCase):

    def test_init_with_empty_dict_creates_graph_of_order_zero(self):
        """Проверяет инициализацию графа пустым словарём."""
        graph = BipartiteGraph({})
        self.assertEqual(graph.order, 0)

    def test_init_with_valid_dict_creates_graph_with_correct_order(self):
        """Проверяет, что порядок графа равен количеству ключей в словаре."""
        adjacency = {0: [1], 1: [0]}
        graph = BipartiteGraph(adjacency)
        self.assertEqual(graph.order, 2)

    def test_init_with_non_dict_input_raises_value_error(self):
        """Проверяет, что передача не-словаря вызывает ValueError."""
        with self.assertRaises(ValueError):
            BipartiteGraph("not a dict")

    def test_init_with_missing_keys_raises_value_error(self):
        """Проверяет, что отсутствие одного из ключей в диапазоне [0, order) вызывает ошибку."""
        adjacency = {0: [0], 2: [1]} 
        with self.assertRaises(ValueError):
            BipartiteGraph(adjacency)

    def test_init_with_non_integer_keys_raises_value_error(self):
        """Проверяет, что нецелочисленный ключ вызывает ValueError."""
        adjacency = {"0": [0], 1: [1]}
        with self.assertRaises(ValueError):
            BipartiteGraph(adjacency)

    def test_init_with_non_list_or_tuple_neighbors_raises_value_error(self):
        """Проверяет, что соседи, заданные не списком и не кортежем, вызывают ошибку."""
        adjacency = {0: "not a list", 1: [0]}
        with self.assertRaises(ValueError):
            BipartiteGraph(adjacency)

    def test_init_with_non_integer_neighbor_raises_value_error(self):
        """Проверяет, что нецелочисленный элемент в списке соседей вызывает ошибку."""
        adjacency = {0: [0.5], 1: [0]}
        with self.assertRaises(ValueError):
            BipartiteGraph(adjacency)

    def test_init_with_neighbor_out_of_range_raises_value_error(self):
        """Проверяет, что сосед с индексом вне [0, order) вызывает ошибку."""
        adjacency = {0: [0], 1: [2]}
        with self.assertRaises(IndexError):
            BipartiteGraph(adjacency)

    def test_right_neighbors_returns_copy_of_neighbors_list(self):
        """Проверяет, что right_neighbors возвращает копию списка соседей."""
        adjacency = {0: [0, 1], 1: [0]}
        graph = BipartiteGraph(adjacency)
        neighbors = graph.right_neighbors(0)
        neighbors.append(99)
        self.assertEqual(graph.right_neighbors(0), [0, 1])

    def test_right_neighbors_returns_empty_list_for_isolated_vertex(self):
        """Проверяет, что для вершины без соседей возвращается пустой список."""
        adjacency = {0: [], 1: [0]}
        graph = BipartiteGraph(adjacency)
        self.assertEqual(graph.right_neighbors(0), [])

    def test_right_neighbors_with_valid_index_returns_correct_list(self):
        """Проверяет корректность возвращаемого списка соседей для допустимого индекса."""
        adjacency = {0: [1, 2], 1: [0, 2], 2: [1]}
        graph = BipartiteGraph(adjacency)
        self.assertEqual(graph.right_neighbors(1), [0, 2])

    def test_right_neighbors_with_out_of_range_index_raises_index_error(self):
        """Проверяет, что запрос соседей для индекса вне [0, order) вызывает IndexError."""
        adjacency = {0: [0], 1: [1]}
        graph = BipartiteGraph(adjacency)
        with self.assertRaises(IndexError):
            graph.right_neighbors(2)

if __name__ == "__main__":
    unittest.main()
