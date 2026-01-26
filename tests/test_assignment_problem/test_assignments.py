import unittest

from assignment_problem.errors.error_message_enum import ErrorMessageEnum
from assignment_problem.hungarian_solver import get_assignments


class TestAssignments(unittest.TestCase):
    """Набор тестов для проверки решения задачи о назначениях."""

    def _check_assignments(self, cost_matrix, cost, assignments):
        """
        Проверяет корректность решения задачи о назначениях.

        :param cost_matrix: Матрица затрат.
        :type cost_matrix: list[list[Number]]
        :param cost: Итоговая стоимость назначения.
        :type cost: Number
        :param assignments: Список назначений в формате (строка, столбец).
        :type assignments: list[tuple[int, int]]

        Проверки:
            - Уникальность строк и столбцов в назначения.
            - Соответствие итоговой стоимости рассчитанной сумме затрат.
            - Корректность типов данных и диапазонов индексов.
        """
        order = len(cost_matrix)
        self.assertIsInstance(assignments, list)
        self.assertEqual(order, len(assignments))
        used_rows = [False] * order
        used_cols = [False] * order
        calculated_cost = 0
        for assignment in assignments:
            self.assertIsInstance(assignment, tuple)
            self.assertEqual(2, len(assignment))
            for idx in assignment:
                self.assertIsInstance(idx, int)
                self.assertLess(idx, order)
            row_idx, col_idx = assignment
            self.assertFalse(used_rows[row_idx])
            self.assertFalse(used_cols[col_idx])
            used_rows[row_idx] = True
            used_cols[col_idx] = True
            calculated_cost += cost_matrix[row_idx][col_idx]
        self.assertEqual(calculated_cost, cost)

    def test_1_order(self):
        """
        Тест для матрицы 1x1.

        Проверяет базовый случай, когда матрица содержит единственный элемент.
        """
        matrix = [[1]]
        result = get_assignments(matrix)
        self.assertEqual(1, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_3_order(self):
        """
        Тест для целочисленной матрицы 3x3.

        Проверяет корректность выполнения алгоритма на небольшой матрице
        с положительными целыми числами.
        """
        matrix = [[10, 10, 8], [9, 8, 1], [9, 7, 4]]
        result = get_assignments(matrix)
        self.assertEqual(18, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_3_float(self):
        """
        Тест для вещественной матрицы 3x3.

        Проверяет обработку матрицы с положительными вещественными числами
        и правильный подсчет итоговой стоимости.
        """
        matrix = [[10.1, 10.2, 8.3], [9.4, 8.5, 1.6], [9.7, 7.8, 4.9]]
        result = get_assignments(matrix)
        self.assertEqual(19.5, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_5_order(self):
        """
        Тест для целочисленной матрицы 5x5.

        Проверяет корректность выполнения алгоритма на матрице среднего размера
        с положительными целыми числами.
        """
        matrix = [
            [12, 9, 27, 10, 23],
            [7, 13, 13, 30, 19],
            [25, 18, 26, 11, 26],
            [9, 28, 26, 23, 13],
            [16, 16, 24, 6, 9],
        ]
        result = get_assignments(matrix)
        self.assertEqual(51, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_5_float(self):
        """
        Тест для вещественной матрицы 5x5.

        Проверяет обработку вещественных чисел в матрице среднего размера,
        включая проверку точности расчетов.
        """
        matrix = [
            [12.01, 9.02, 27.03, 10.04, 23.05],
            [7.06, 13.07, 13.08, 30.09, 19.1],
            [25.11, 18.12, 26.13, 11.14, 26.15],
            [9.16, 28.17, 26.18, 23.19, 13.2],
            [16.21, 16.22, 24.23, 6.24, 9.25],
        ]
        result = get_assignments(matrix)
        self.assertAlmostEqual(51.65, result.cost, places=2)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_10_order(self):
        """
        Тест для целочисленной матрицы 10x10.

        Проверяет производительность и корректность выполнения алгоритма
        на большой матрице с положительными целыми числами.
        """
        matrix = [
            [37, 34, 29, 26, 19, 8, 9, 23, 19, 29],
            [9, 28, 20, 8, 18, 20, 14, 33, 23, 14],
            [15, 26, 12, 28, 6, 17, 9, 13, 21, 7],
            [2, 8, 38, 36, 39, 5, 36, 2, 38, 27],
            [30, 3, 33, 16, 21, 39, 7, 23, 28, 36],
            [7, 5, 19, 22, 36, 36, 24, 19, 30, 2],
            [34, 20, 13, 36, 12, 33, 9, 10, 23, 5],
            [7, 37, 22, 39, 33, 39, 10, 3, 13, 26],
            [21, 25, 23, 39, 31, 37, 32, 33, 38, 1],
            [17, 34, 40, 10, 29, 37, 40, 3, 25, 3],
        ]
        result = get_assignments(matrix)
        self.assertEqual(66, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_10_float(self):
        """
        Тест для вещественной матрицы 10x10.

        Проверяет производительность и корректность выполнения алгоритма
        на большой матрице с положительными вещественными числами.
        """
        matrix = [
            [
                37.001,
                34.002,
                29.003,
                26.004,
                19.005,
                8.006,
                9.007,
                23.008,
                19.009,
                29.01,
            ],
            [
                9.011,
                28.012,
                20.013,
                8.014,
                18.015,
                20.016,
                14.017,
                33.018,
                23.019,
                14.02,
            ],
            [
                15.021,
                26.022,
                12.023,
                28.024,
                6.025,
                17.026,
                9.027,
                13.028,
                21.029,
                7.03,
            ],
            [2.031, 8.032, 38.033, 36.034, 39.035, 5.036, 36.037, 2.038, 38.039, 27.04],
            [
                30.041,
                3.042,
                33.043,
                16.044,
                21.045,
                39.046,
                7.047,
                23.048,
                28.049,
                36.05,
            ],
            [
                7.051,
                5.052,
                19.053,
                22.054,
                36.055,
                36.056,
                24.057,
                19.058,
                30.059,
                2.06,
            ],
            [
                34.061,
                20.062,
                13.063,
                36.064,
                12.065,
                33.066,
                9.067,
                10.068,
                23.069,
                5.07,
            ],
            [
                7.071,
                37.072,
                22.073,
                39.074,
                33.075,
                39.076,
                10.077,
                3.078,
                13.079,
                26.08,
            ],
            [
                21.081,
                25.082,
                23.083,
                39.084,
                31.085,
                37.086,
                32.087,
                33.088,
                38.089,
                1.09,
            ],
            [
                17.091,
                34.092,
                40.093,
                10.094,
                29.095,
                37.096,
                40.097,
                3.098,
                25.099,
                3.1,
            ],
        ]
        result = get_assignments(matrix)
        self.assertAlmostEqual(66.505, result.cost, places=3)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_20_order(self):
        """
        Тест для целочисленной матрицы 20x20.

        Проверяет производительность и корректность выполнения алгоритма
        на большой матрице с положительными целыми числами.
        """
        matrix = [
            [5, 4, 3, 9, 8, 9, 3, 5, 6, 9, 4, 10, 3, 5, 6, 6, 1, 8, 10, 2],
            [10, 9, 9, 2, 8, 3, 9, 9, 10, 1, 7, 10, 8, 4, 2, 1, 4, 8, 4, 8],
            [10, 4, 4, 3, 1, 3, 5, 10, 6, 8, 6, 8, 4, 10, 7, 2, 4, 5, 1, 8],
            [2, 1, 4, 2, 3, 9, 3, 4, 7, 3, 4, 1, 3, 2, 9, 8, 6, 5, 7, 8],
            [3, 4, 4, 1, 4, 10, 1, 2, 6, 4, 5, 10, 2, 2, 3, 9, 10, 9, 9, 10],
            [1, 10, 1, 8, 1, 3, 1, 7, 1, 1, 2, 1, 2, 6, 3, 3, 4, 4, 8, 6],
            [1, 8, 7, 10, 10, 3, 4, 6, 1, 6, 6, 4, 9, 6, 9, 6, 4, 5, 4, 7],
            [8, 10, 3, 9, 4, 9, 3, 3, 4, 6, 4, 2, 6, 7, 7, 4, 4, 3, 4, 7],
            [1, 3, 8, 2, 6, 9, 2, 7, 4, 8, 10, 8, 10, 5, 1, 3, 10, 10, 2, 9],
            [2, 4, 1, 9, 2, 9, 7, 8, 2, 1, 4, 10, 5, 2, 7, 6, 5, 7, 2, 6],
            [4, 5, 1, 4, 2, 3, 3, 4, 1, 8, 8, 2, 6, 9, 5, 9, 6, 3, 9, 3],
            [3, 1, 1, 8, 6, 8, 8, 7, 9, 3, 2, 1, 8, 2, 4, 7, 3, 1, 2, 4],
            [5, 9, 8, 6, 10, 4, 10, 3, 4, 10, 10, 10, 1, 7, 8, 8, 7, 7, 8, 8],
            [1, 4, 6, 1, 6, 1, 2, 10, 5, 10, 2, 6, 2, 4, 5, 5, 3, 5, 1, 5],
            [5, 6, 9, 10, 6, 6, 10, 6, 4, 1, 5, 3, 9, 5, 2, 10, 9, 9, 5, 1],
            [10, 9, 4, 6, 9, 5, 3, 7, 10, 1, 6, 8, 1, 1, 10, 9, 5, 7, 7, 5],
            [2, 6, 6, 6, 6, 2, 9, 4, 7, 5, 3, 2, 10, 3, 4, 5, 10, 9, 1, 7],
            [5, 2, 4, 9, 8, 4, 8, 2, 4, 1, 3, 7, 6, 8, 1, 6, 8, 8, 10, 10],
            [9, 6, 3, 1, 8, 5, 7, 8, 7, 2, 1, 8, 2, 8, 3, 7, 4, 8, 7, 7],
            [8, 4, 4, 9, 7, 10, 6, 2, 1, 5, 8, 5, 1, 1, 1, 9, 1, 3, 5, 3],
        ]
        result = get_assignments(matrix)
        self.assertEqual(22, result.cost)
        self._check_assignments(matrix, result.cost, result.assignments)

    def test_none(self):
        """
        Проверяет выброс исключения при передаче `None` в качестве параметра.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке при передаче недопустимого значения `None`.

        Исключение:
            - ValueError: Если передан `None`.
        """
        self.assertRaisesRegex(ValueError, ErrorMessageEnum.WRONG_MATRIX, get_assignments, None)

    def test_empty(self):
        """
        Проверяет выброс исключения при передаче пустого списка в качестве параметра.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке при передаче пустой матрицы.

        Исключение:
            - ValueError: Если передан пустой список.
        """
        self.assertRaisesRegex(ValueError, ErrorMessageEnum.WRONG_MATRIX, get_assignments, [])

    def test_empty_row(self):
        """
        Проверяет выброс исключения при передаче списка с пустым списком в качестве параметра.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке при передаче матрицы с пустой строкой.

        Исключение:
            - ValueError: Если передан список, содержащий пустую строку.
        """
        self.assertRaisesRegex(ValueError, ErrorMessageEnum.WRONG_MATRIX, get_assignments, [[]])

    def test_incorrect_values(self):
        """
        Проверяет выброс исключения при наличии некорректных значений в матрице.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке, если в матрице присутствуют недопустимые значения
        (например, `None`, строка или вложенный список).

        Примеры некорректных значений:
            - None
            - "str"
            - []

        Исключение:
            - ValueError: Если в матрице обнаружены некорректные значения.
        """
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            self.assertRaisesRegex(
                ValueError, ErrorMessageEnum.WRONG_MATRIX, get_assignments, [[1, value]]
            )

    def test_jag(self):
        """
        Проверяет выброс исключения при наличии строк разной длины в матрице.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке, если строки матрицы имеют разную длину.

        Исключение:
            - ValueError: Если строки матрицы имеют разную длину.
        """
        matrix = [[1.0, 2.0, 3.0], [1.0, 2.0]]
        self.assertRaisesRegex(ValueError, ErrorMessageEnum.WRONG_MATRIX, get_assignments, matrix)

    def test_negative_value(self):
        """
        Проверяет выброс исключения при наличии отрицательных значений в матрице.

        Убедитесь, что функция выбрасывает исключение `ValueError` с корректным
        сообщением об ошибке, если матрица содержит отрицательные значения.

        Исключение:
            - ValueError: Если в матрице обнаружены отрицательные значения.
        """
        with self.assertRaises(ValueError) as error:
            get_assignments([[1, -1], [1, 2]])
        self.assertEqual(ErrorMessageEnum.WRONG_MATRIX, str(error.exception))


if __name__ == "__main__":
    unittest.main()
