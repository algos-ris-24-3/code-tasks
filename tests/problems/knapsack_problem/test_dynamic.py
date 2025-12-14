import unittest

from problems.knapsack_problem.dynamic_solver import DynamicSolver
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum
from tests.problems.knapsack_problem.test_abstract import TestAbstractSolver


class TestDynamicSolver(unittest.TestCase, TestAbstractSolver):
    """Набор тестов для проверки решения задачи о рюкзаке методом
    динамического программирования."""

    solver = DynamicSolver

    def test_float_in_weights(self):
        """Проверяет выброс исключения при передаче не целочисленного значения
        в списке весов."""
        with self.assertRaises(ValueError) as error:
            self.solver([1, 1.1], [1, 1], 1)
        self.assertEqual(
            ErrorMessageEnum.FLOAT_WEIGHT,
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
