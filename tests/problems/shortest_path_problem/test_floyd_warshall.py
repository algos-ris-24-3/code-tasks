import unittest

from problems.shortest_path_problem import ShortestPath
from problems.shortest_path_problem.errors.error_message_enum import ErrorMessageEnum
from problems.shortest_path_problem.floyd_warshall import get_shortest_path


class TestFloydWarshall(unittest.TestCase):
    def test_none_matrix(self):
        """Проверяет, что вызов функции с матрицей, равной None, вызывает исключение с
        ожидаемым сообщением о невалидной матрице"""
        self.assertRaisesRegex(
            ValueError, ErrorMessageEnum.WRONG_MATRIX, get_shortest_path, None, 0, 1
        )

    def test_empty_matrix(self):
        """Проверяет, что вызов функции с пустой матрицей вызывает исключение с
        ожидаемым сообщением о пустой матрице"""
        self.assertRaisesRegex(
            ValueError, ErrorMessageEnum.EMPTY_MATRIX, get_shortest_path, [], 0, 1
        )

    def test_src_incorrect(self):
        """Проверяет, что некорректный индекс исходной вершины вызывает
        соответствующее исключение"""
        matrix = [[3, 3], [3, 2]]
        for value in [-1, 2, 1.1, "str", None]:
            self.assertRaisesRegex(
                ValueError,
                ErrorMessageEnum.WRONG_SRC,
                get_shortest_path,
                matrix,
                value,
                1,
            )

    def test_trg_incorrect(self):
        """Проверяет, что некорректный индекс целевой вершины вызывает
        соответствующее исключение"""
        matrix = [[3, 3], [3, 2]]
        for value in [-1, 2, 1.1, "str", None]:
            self.assertRaisesRegex(
                ValueError,
                ErrorMessageEnum.WRONG_TRG,
                get_shortest_path,
                matrix,
                1,
                value,
            )

    def test_not_square_rectangle(self):
        """Проверяет, что прямоугольная матрица вызывает исключение
        о неквадратной матрице"""
        matrix = [[3, 3, 5], [3, 2, 4]]
        self.assertRaisesRegex(
            ValueError, ErrorMessageEnum.WRONG_MATRIX, get_shortest_path, matrix, 1, 2
        )

    def test_not_square_jag(self):
        """Проверяет, что "рваная" матрица (с разным числом элементов в строках)
        вызывает исключение о неквадратной матрице"""
        matrix = [[3, 3, 5, 8], [3, 2, 4, 6], [2, 5, 7]]
        self.assertRaisesRegex(
            ValueError, ErrorMessageEnum.WRONG_MATRIX, get_shortest_path, matrix, 1, 2
        )

    def test_single(self):
        """Проверяет случай матрицы размера 1×1, где исходная и целевая вершины совпадают"""
        matrix = [[1]]
        self.assertEqual(get_shortest_path(matrix, 0, 0), ShortestPath(0, []))

    def test_double(self):
        """Проверяет простой случай матрицы размера 2×2 с единственным путём между вершинами"""
        matrix = [[None, 1], [None, None]]
        self.assertEqual(get_shortest_path(matrix, 0, 1), ShortestPath(1, [0, 1]))

    def test_disconnected(self):
        """Проверяет случай, когда вершины не связаны друг с другом"""
        matrix = [
            [0, 1, None, None],
            [None, 0, 1, None],
            [None, None, 0, None],
            [None, None, None, 0],
        ]
        self.assertEqual(get_shortest_path(matrix, 0, 3), ShortestPath(None, []))

    def test_revers_order(self):
        """Проверяет, что алгоритм корректно работает, если путь между ними в
        ориентированном графе невозможен"""
        matrix = [[0, None, None], [1, 0, None], [None, 1, 0]]
        self.assertEqual(get_shortest_path(matrix, 0, 2), ShortestPath(None, []))

    def test_unordered(self):
        """Проверяет, что алгоритм корректно работает для неориентированного графа"""
        matrix = [[0, 1, None], [1, 0, 1], [None, 1, 0]]
        self.assertEqual(get_shortest_path(matrix, 0, 2), ShortestPath(2, [0, 1, 2]))

    def test_ordered_with_loop(self):
        """Проверяет случай, когда в ориентированном графе есть цикл"""
        matrix = [
            [None, 1, 2, None],
            [None, None, None, 2],
            [None, None, None, 2],
            [1, None, None, None],
        ]
        self.assertEqual(get_shortest_path(matrix, 0, 3), ShortestPath(3, [0, 1, 3]))

    def test_1(self):
        """Пример 1"""
        matrix = [
            [0, 2, None, 3, None, None],
            [None, 0, 1, None, 4, None],
            [None, None, 0, None, None, 5],
            [None, None, None, 0, 2, None],
            [None, None, None, None, 0, 1],
            [None, None, None, None, None, 0],
        ]
        self.assertEqual(
            get_shortest_path(matrix, 0, 5),
            ShortestPath(6, [0, 3, 4, 5]),
        )

    def test_2(self):
        """Пример 2"""
        matrix = [
            [0, 10, 30, 50, 10],
            [None, 0, None, None, None],
            [None, None, 0, None, 10],
            [None, 40, 20, 0, None],
            [10, None, 10, 30, 0],
        ]
        self.assertEqual(
            get_shortest_path(matrix, 0, 3),
            ShortestPath(40, [0, 4, 3]),
        )

    def test_3(self):
        """Пример 3"""
        matrix = [
            [0, 7, 9, None, None, 14],
            [7, 0, 10, 15, None, None],
            [9, 10, 0, 11, None, 2],
            [None, 15, 11, 0, 6, None],
            [None, None, None, 6, 0, 9],
            [14, None, 2, None, 9, 0],
        ]
        self.assertEqual(
            get_shortest_path(matrix, 0, 5),
            ShortestPath(11, [0, 2, 5]),
        )

    def test_has_negative(self):
        """Пример с отрицательным значением в матрице"""
        matrix = [[None, 2, 2], [None, None, -1], [None, None, None]]
        self.assertEqual(
            get_shortest_path(matrix, 0, 2),
            ShortestPath(1, [0, 1, 2]),
        )

    def test_has_negative_loop(self):
        """Пример с отрицательным циклом"""
        matrix = [
            [None, 1, None, None],
            [None, None, 4, -3],
            [3, None, None, None],
            [1, None, 2, None],
        ]
        self.assertRaisesRegex(
            RuntimeError,
            ErrorMessageEnum.NEGATIVE_LOOP,
            get_shortest_path,
            matrix,
            1,
            2,
        )

    def test_4(self):
        """Проверяет корректность работы алгоритма на крупной матрице,
        где для каждой пары вершин сравниваются результаты с
        предопределёнными минимальными расстояниями"""
        matrix = [
            [None, 8, 2, None, 13, 10, 8, None, 10, 9],
            [2, None, 7, None, 4, 11, 12, None, 1, 5],
            [3, 14, None, 4, 13, 5, None, 14, 9, 11],
            [6, 2, 3, None, 10, 5, 13, 12, 2, 2],
            [3, 13, 3, 3, None, 10, 3, 6, 5, None],
            [7, 1, 6, 3, 5, None, 8, 14, None, 6],
            [7, None, 10, 8, 11, 13, None, 14, 2, 4],
            [13, 7, 5, 1, None, 9, 1, None, 3, 7],
            [6, 11, None, 15, 1, 15, 11, 4, None, 10],
            [7, 10, 10, 6, 12, None, 7, None, 14, None],
        ]
        min_distances = [
            [0, 8, 2, 6, 9, 7, 8, 12, 8, 8],
            [2, 0, 4, 5, 2, 9, 5, 5, 1, 5],
            [3, 6, 0, 4, 7, 5, 10, 10, 6, 6],
            [4, 2, 3, 0, 3, 5, 6, 6, 2, 2],
            [3, 5, 3, 3, 0, 8, 3, 6, 5, 5],
            [3, 1, 5, 3, 3, 0, 6, 6, 2, 5],
            [6, 8, 6, 6, 3, 11, 0, 6, 2, 4],
            [5, 3, 4, 1, 4, 6, 1, 0, 3, 3],
            [4, 6, 4, 4, 1, 9, 4, 4, 0, 6],
            [7, 8, 9, 6, 9, 11, 7, 12, 8, 0],
        ]
        for row_idx in range(len(matrix)):
            for col_idx in range(len(matrix)):
                expected_distance = min_distances[row_idx][col_idx]
                result = get_shortest_path(matrix, row_idx, col_idx)
                self.__check_result(expected_distance, matrix, result)

    def __check_result(self, expected_distance, matrix, result):
        """Проверяет, что расстояние и путь, возвращённые алгоритмом,
        соответствуют ожиданиям. Также проверяет целостность пути"""
        self.assertEqual(expected_distance, result.distance)
        if result.distance:
            dist_by_path = self.__get_dist_by_path(result.path, matrix)
            self.assertEqual(result.distance, dist_by_path)
        else:
            result.path == []

    def __get_dist_by_path(self, path, matrix):
        """Вычисляет расстояние по заданному пути и матрице, чтобы убедиться
        в соответствии результата ожидаемому."""
        if not path:
            return None
        if len(path) < 2:
            raise Exception("Incorrect path")
        total_dist = 0
        for idx in range(1, len(path)):
            row_idx = path[idx - 1]
            col_idx = path[idx]
            dist = matrix[row_idx][col_idx]
            if dist is None:
                raise Exception(f"Incorrect path {row_idx} -> {col_idx}")
            total_dist += dist
        return total_dist


if __name__ == "__main__":
    unittest.main()
