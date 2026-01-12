from abc import ABC
import random
from problems.tsp_problem.errors.error_message_enum import ErrorMessageEnum
from problems.tsp_problem.tsp_abs_solver import NullableNumber, TspSolution


class TestAbstractTspSolver(ABC):
    """Набор тестов для проверки решения задачи о рюкзаке методом полного
    перебора."""

    solver = None

    @staticmethod
    def __check_path(
        matrix: list[list[NullableNumber]], result: dict[str, float | list[int]]
    ) -> bool:
        """Проверяет корректность найденного пути."""
        distance = result.distance
        path = result.path
        if len(matrix) + 1 != len(path):
            return False
        if len(matrix) == 1 and path != [0]:
            return False
        if path[0] != path[-1]:
            return False
        if set(path) != set([n for n in range(len(matrix))]):
            return False
        total_dist = 0
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            total_dist += matrix[src][trg]
        if total_dist != distance:
            return False
        return True

    def test_incorrect_matrix(self):
        """Проверяет выброс исключения при передаче некорректного значения
        матрицы."""
        incorrect_values = [None, [], [[]], (), {}, "str", 1, 1.1]
        for value in incorrect_values:
            self.assertRaisesRegex(
                TypeError,
                ErrorMessageEnum.WRONG_MATRIX,
                self.solver,
                value,
            )

    def test_not_square_rectangle(self):
        """Проверяет выброс исключения при передаче не прямоугольной матрицы."""
        matrix = [[3.0, 3.0, 5.0], [3.0, 2.0, 4.0]]
        self.assertRaisesRegex(
            TypeError,
            ErrorMessageEnum.WRONG_MATRIX,
            self.solver,
            matrix,
        )

    def test_not_square_jag(self):
        """Проверяет выброс исключения при передаче рваной матрицы."""
        matrix = [[3.0, 3.0, 5.0], [3.0, 2.0], [2.0, 5.0, 7.0]]
        self.assertRaisesRegex(
            TypeError,
            ErrorMessageEnum.WRONG_MATRIX,
            self.solver,
            matrix,
        )

    def test_has_not_number(self):
        """Проверяет выброс исключения при наличии в матрице нечислового
        значения."""
        matrix = [["str", 3.0], [3.0, 2.0]]
        self.assertRaisesRegex(
            TypeError,
            ErrorMessageEnum.WRONG_MATRIX,
            self.solver,
            matrix,
        )

    def test_has_negative_number(self):
        """Проверяет выброс исключения при наличии в матрице отрицательного
        значения."""
        matrix = [[1, 3.0], [3.0, -0.1]]
        self.assertRaisesRegex(
            ValueError,
            ErrorMessageEnum.NEG_VALUE,
            self.solver,
            matrix,
        )

    def test_single(self):
        """Проверяет построение маршрута в матрице единичного порядка."""
        matrix = [[None]]
        solver = self.solver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(0, [0]))

    def test_double(self):
        """Проверяет построение маршрута в матрице второго порядка."""
        matrix = [[None, 1.0], [2.0, None]]
        solver = self.solver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(3, [0, 1, 0]))

    def test_has_not_path(self):
        """Проверяет вывод данных при отсутствии маршрута в матрице."""
        matrix = [[None, 1.0], [None, None]]
        solver = self.solver(matrix)
        self.assertEqual(solver.get_tsp_solution(), TspSolution(None, []))

    def test_triple(self):
        """Проверяет построение маршрута в матрице третьего порядка."""
        matrix = [[None, 1.0, 2.0], [4.0, None, 3.0], [None, 5.0, 6.0]]
        solver = self.solver(matrix)
        result = solver.get_tsp_solution()
        self.assertEqual(result.distance, 11.0)
        self.assertTrue(self.__check_path(matrix, result))

    def test_four(self):
        """Проверяет построение маршрута в матрице четвертого порядка."""
        matrix = [
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
            [9.0, 10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0, 16.0],
        ]
        solver = self.solver(matrix)
        result = solver.get_tsp_solution()
        self.assertEqual(result.distance, 34.0)
        self.assertTrue(self.__check_path(matrix, result))

    def test_pentad(self):
        """Проверяет построение маршрута в матрице пятого порядка."""
        matrix = [
            [None, 12.0, 9.0, 9.0, 12.0],
            [9.0, None, 8.0, 19.0, 15.0],
            [7.0, 1.0, None, 17.0, 11.0],
            [5.0, 9.0, 12.0, None, 16.0],
            [14.0, 6.0, 12.0, 22.0, None],
        ]
        solver = self.solver(matrix)
        result = solver.get_tsp_solution()
        self.assertEqual(result.distance, 46.0)
        self.assertTrue(self.__check_path(matrix, result))

    def test_random_simple(self):
        """Проверяет построение маршрута в простой случайной матрице."""
        order = random.randint(3, 9)
        value = float(random.randint(1, 100))
        matrix = [[value for _ in range(order)] for _ in range(order)]
        solver = self.solver(matrix)
        result = solver.get_tsp_solution()
        self.assertEqual(result.distance, order * value)
        self.assertTrue(self.__check_path(matrix, result))

    def test_random(self):
        """Проверяет построение маршрута в случайной матрице."""
        order = random.randint(3, 9)
        path = [n for n in range(1, order)]
        random.shuffle(path)
        path = [0] + path + [0]
        value = 1.0
        distance = 0
        matrix = [[None for _ in range(order)] for _ in range(order)]
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            matrix[src][trg] = value
            distance += value
            value += 1.0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] is None:
                    matrix[i][j] = value + float(random.randint(1, 100))
        solver = self.solver(matrix)
        result = solver.get_tsp_solution()

        self.assertEqual(result.distance, distance)
        self.assertTrue(self.__check_path(matrix, result))
