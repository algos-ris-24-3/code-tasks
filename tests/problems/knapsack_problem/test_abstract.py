from abc import ABC

from problems.knapsack_problem.errors.constants import COSTS, WEIGHTS
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum
from problems.knapsack_problem.errors.error_message_template import (
    ErrorMessageTemplateEnum,
)
from tests.problems.knapsack_problem import check_knapsack_items


class TestAbstractSolver(ABC):
    """Набор тестов для проверки решения задачи о рюкзаке методом полного
    перебора."""

    solver = None

    def test_2(self):
        """Проверка решения задачи о рюкзаке для двух предметов."""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 2)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_3(self):
        """Проверка решения задачи о рюкзаке для трех предметов."""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 3)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_4(self):
        """Проверка решения задачи о рюкзаке для четырех предметов."""
        weights = [1, 2, 3, 4]
        costs = [1, 2, 3, 4]
        weight_limit = 4
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 4)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_5(self):
        """Проверка решения задачи о рюкзаке для пяти предметов."""
        weights = [10, 5, 12, 4, 2]
        costs = [5, 5, 3, 8, 6]
        weight_limit = 20
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 19)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_6(self):
        """Проверка решения задачи о рюкзаке для шести предметов."""
        weights = [10, 5, 12, 4, 2, 2]
        costs = [5, 5, 3, 8, 6, 8]
        weight_limit = 20
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 27)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_7(self):
        """Проверка решения задачи о рюкзаке для семи предметов."""
        weights = [10, 6, 11, 4, 1, 4, 3]
        costs = [15, 10, 22, 7, 1, 9, 4]
        weight_limit = 20
        solver = self.solver(weights, costs, weight_limit)
        result = solver.get_knapsack()
        self.assertEqual(result.cost, 39)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_not_list_weights(self):
        """Проверяет выброс исключения при передаче некорректного списка
        весов."""
        with self.assertRaises(TypeError) as error:
            self.solver(1, [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_LIST.format(WEIGHTS),
            str(error.exception),
        )

    def test_not_list_costs(self):
        """Проверяет выброс исключения при передаче некорректного списка
        стоимостей."""
        with self.assertRaises(TypeError) as error:
            self.solver([1], "str", 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_LIST.format(COSTS),
            str(error.exception),
        )

    def test_empty_weights(self):
        """Проверяет выброс исключения при передаче пустого списка
        весов."""
        with self.assertRaises(ValueError) as error:
            self.solver([], [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.EMPTY_LIST.format(WEIGHTS),
            str(error.exception),
        )

    def test_empty_costs(self):
        """Проверяет выброс исключения при передаче пустого списка
        стоимостей."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.EMPTY_LIST.format(COSTS),
            str(error.exception),
        )

    def test_not_int_in_weights(self):
        """Проверяет выброс исключения при передаче нечислового значения
        в списке весов."""
        with self.assertRaises(TypeError) as error:
            self.solver([1, "str"], [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_INT.format(WEIGHTS),
            str(error.exception),
        )

    def test_not_int_in_costs(self):
        """Проверяет выброс исключения при передаче нечислового значения
        в списке стоимостей."""
        with self.assertRaises(TypeError) as error:
            self.solver([1], [0.1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_INT.format(COSTS),
            str(error.exception),
        )

    def test_zero_in_weights(self):
        """Проверяет выброс исключения при передаче нулевого значения
        в списке весов."""
        with self.assertRaises(ValueError) as error:
            self.solver([1, 0], [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_POS.format(WEIGHTS),
            str(error.exception),
        )

    def test_zero_in_costs(self):
        """Проверяет выброс исключения при передаче нулевого значения
        в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [0], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_POS.format(COSTS),
            str(error.exception),
        )

    def test_neg_in_weights(self):
        """Проверяет выброс исключения при передаче отрицательного значения
        в списке весов."""
        with self.assertRaises(ValueError) as error:
            self.solver([1, -1], [1, 1], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_POS.format(WEIGHTS),
            str(error.exception),
        )

    def test_neg_in_costs(self):
        """Проверяет выброс исключения при передаче отрицательного значения
        в списке стоимостей."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [-10], 1)
        self.assertEqual(
            ErrorMessageTemplateEnum.NOT_POS.format(COSTS),
            str(error.exception),
        )

    def test_diff_len(self):
        """Проверяет выброс исключения при передаче списков весов и
        стоимостей разной длины."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [1, 1], 1)
        self.assertEqual(ErrorMessageEnum.LENGTHS_NOT_EQUAL, str(error.exception))

    def test_not_int_limit(self):
        """Проверяет выброс исключения при указании нечислового ограничения
        вместимости рюкзака."""
        with self.assertRaises(TypeError) as error:
            self.solver([1], [1], 1.1)
        self.assertEqual(ErrorMessageEnum.NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_zero_limit(self):
        """Проверяет выброс исключения при указании нулевого ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [1], 0)
        self.assertEqual(ErrorMessageEnum.NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_neg_limit(self):
        """Проверяет выброс исключения при указании отрицательного ограничения
        вместимости рюкзака."""
        with self.assertRaises(ValueError) as error:
            self.solver([1], [1], -2)
        self.assertEqual(ErrorMessageEnum.NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_min_limit(self):
        """Проверяет выброс исключения при указании ограничения вместимости
        рюкзака менее чем минимальный вес предмета."""
        with self.assertRaises(ValueError) as error:
            self.solver([2], [1], 1)
        self.assertEqual(ErrorMessageEnum.LESS_WEIGHT_LIMIT, str(error.exception))
