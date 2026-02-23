import unittest


from network_flow.error_message_enum import ErrorMessageEnum
from network_flow.max_flow_calculator import CAPACITY_MATRIX_NAME
from network_flow.min_cost_flow_calculator import (
    COST_MATRIX_NAME,
    MinCostFlowCalculator,
)
from tests.network_flow.test_max_flow import TestMaxFlow


class TestMinCostFlow(TestMaxFlow):
    """Набор тестов для проверки решения задачи о максимальном потоке минимальной стоимости."""

    default_capacity_matrix = [
        # s  t
        [0, 1],  # s
        [0, 0],  # t
    ]
    default_cost_matrix = [
        # s  t
        [0, 2],  # s
        [0, 0],  # t
    ]

    def _check_cost(self, flow_matrix, cost_matrix, expected_min_cost):
        total_cost = 0
        for row_idx in range(len(flow_matrix)):
            for col_idx in range(len(flow_matrix)):
                total_cost += (
                    flow_matrix[row_idx][col_idx] * cost_matrix[row_idx][col_idx]
                    if flow_matrix[row_idx][col_idx]
                    else 0
                )
        self.assertEqual(expected_min_cost, total_cost)

    def test_2_order(self):
        """Проверяет поиск максимального потока для сети из 2 вершин"""
        expected_cost = 2
        result = MinCostFlowCalculator(
            self.default_capacity_matrix, self.default_cost_matrix
        )
        self.assertEqual(1, result._max_flow)
        self._check_max_flow(
            self.default_capacity_matrix, result._flow_matrix, result._max_flow
        )
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, self.default_cost_matrix, expected_cost)

    def test_3_order(self):
        """Проверяет поиск максимального потока для сети из 3 вершин"""
        capacity_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [0, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  t
            [0, 1, 0],  # s
            [0, 0, 2],  # a
            [0, 0, 0],  # t
        ]
        expected_cost = 6
        expected_flow = 2
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_4_order(self):
        """Проверяет поиск максимального потока для сети из 3 вершин
        graph LR
        s-->|2/1$|a
        s-->|1/1$|b
        a-->|1/1$|b
        a-->|3/5$|t
        b-->|3/1$|t
        """
        capacity_matrix = [
            # s a  b  t
            [0, 2, 1, 0],  # s
            [0, 0, 1, 3],  # a
            [0, 0, 0, 3],  # b
            [0, 0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  b  t
            [0, 1, 1, 0],  # s
            [0, 0, 1, 5],  # a
            [0, 0, 0, 1],  # b
            [0, 0, 0, 0],  # t
        ]
        expected_cost = 11
        expected_flow = 3
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_5_order(self):
        """Проверяет поиск максимального потока для сети из 5 вершин
        graph LR
        s-->|7/1$|a
        s-->|6/5$|c
        a-->|3/1$|b
        a-->|6/1$|c
        a-->|3/1$|t
        b-->|5/1$|c
        b-->|2/1$|t
        c-->|3/1$|t
        """
        capacity_matrix = [
            # s a  b  c  t
            [0, 7, 0, 6, 0],  # s
            [0, 0, 3, 6, 3],  # a
            [0, 0, 0, 5, 2],  # b
            [0, 0, 0, 0, 3],  # c
            [0, 0, 0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  b  c  t
            [0, 1, 0, 5, 0],  # s
            [0, 0, 1, 1, 1],  # a
            [0, 0, 0, 1, 1],  # b
            [0, 0, 0, 0, 1],  # c
            [0, 0, 0, 0, 0],  # t
        ]
        expected_cost = 24
        expected_flow = 8
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_6_order(self):
        """Проверяет поиск максимального потока для сети из 6 вершин
        graph LR
        s-->|7/3$|a
        s-->|7/2$|b
        s-->|7/4$|c
        a-->|9/5$|d
        b-->|5/2$|c
        b-->|6/2$|a
        c-->|11/2$|d
        a-->|6/4$|c
        d-->|13/1$|t
        """
        capacity_matrix = [
            # s a  b  c  d  t
            [0, 7, 7, 7, 0, 0],  # s
            [0, 0, 0, 6, 9, 0],  # a
            [0, 6, 0, 5, 0, 0],  # b
            [0, 0, 0, 0, 11, 0],  # c
            [0, 0, 0, 0, 0, 13],  # d
            [0, 0, 0, 0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  b  c  d  t
            [0, 3, 2, 4, 0, 0],  # s
            [0, 0, 0, 4, 5, 0],  # a
            [0, 2, 0, 2, 0, 0],  # b
            [0, 0, 0, 0, 2, 0],  # c
            [0, 0, 0, 0, 0, 1],  # d
            [0, 0, 0, 0, 0, 0],  # t
        ]
        expected_cost = 95
        expected_flow = 13
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_6_order_with_loop(self):
        """Проверяет поиск максимального потока для сети из 3 вершин с циклом
        graph LR
        s-->|3/1$|a
        s-->|6/5$|b
        a-->|2/1$|b
        c-->|5/1$|a
        b-->|4/1$|c
        b-->|7/5$|d
        c-->|8/1$|d
        d-->|12/1$|t
        """
        capacity_matrix = [
            # s a  b  c  d  t
            [0, 3, 6, 0, 0, 0],  # s
            [0, 0, 2, 0, 0, 0],  # a
            [0, 0, 0, 4, 7, 0],  # b
            [0, 5, 0, 0, 8, 0],  # c
            [0, 0, 0, 0, 0, 12],  # d
            [0, 0, 0, 0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  b  c  d  t
            [0, 1, 5, 0, 0, 0],  # s
            [0, 0, 1, 0, 0, 0],  # a
            [0, 0, 0, 1, 5, 0],  # b
            [0, 1, 0, 0, 1, 0],  # c
            [0, 0, 0, 0, 0, 1],  # d
            [0, 0, 0, 0, 0, 0],  # t
        ]
        expected_cost = 70
        expected_flow = 8
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_10_order(self):
        """Проверяет поиск максимального потока для сети из 10 вершин
        graph LR
        s-->|7/1$|a
        s-->|6/2$|b
        s-->|5/1$|c
        a-->|8/1$|d
        b-->|5/1$|e
        b-->|6/1$|h
        c-->|3/1$|b
        c-->|5/1$|f
        d-->|4/1$|b
        d-->|4/1$|g
        e-->|8/1$|t
        f-->|3/1$|h
        f-->|3/3$|t
        g-->|3/1$|e
        g-->|3/3$|t
        h-->|10/1$|t
        """
        capacity_matrix = [
            # s a  b  c  d  e  f  g  h  t
            [0, 7, 6, 5, 0, 0, 0, 0, 0, 0],  # s
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],  # a
            [0, 0, 0, 0, 0, 5, 0, 0, 6, 0],  # b
            [0, 0, 3, 0, 0, 0, 5, 0, 0, 0],  # c
            [0, 0, 4, 0, 0, 0, 0, 4, 0, 0],  # d
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],  # e
            [0, 0, 0, 0, 0, 0, 0, 0, 3, 3],  # f
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 2],  # g
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 10],  # h
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # t
        ]
        cost_matrix = [
            # s a  b  c  d  e  f  g  h  t
            [0, 1, 2, 1, 0, 0, 0, 0, 0, 0],  # s
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # a
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],  # b
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # c
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # d
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # e
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 3],  # f
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 3],  # g
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # h
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # t
        ]
        expected_cost = 80
        expected_flow = 18
        result = MinCostFlowCalculator(capacity_matrix, cost_matrix)
        self.assertEqual(expected_flow, result._max_flow)
        self._check_max_flow(capacity_matrix, result._flow_matrix, result._max_flow)
        self.assertEqual(expected_cost, result._min_cost)
        self._check_cost(result._flow_matrix, cost_matrix, expected_cost)

    def test_none(self):
        """Проверяет выброс исключения при передаче `None` в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            None,
            self.default_cost_matrix,
        )
        self.assertRaisesRegex(
            ValueError,
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            self.default_capacity_matrix,
            None,
        )

    def test_empty(self):
        """Проверяет выброс исключения при передаче пустого списка в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            [],
            self.default_cost_matrix,
        )
        self.assertRaisesRegex(
            ValueError,
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            self.default_capacity_matrix,
            [],
        )

    def test_empty_row(self):
        """Проверяет выброс исключения при передаче списка с пустым списком в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            [[]],
            self.default_cost_matrix,
        )
        self.assertRaisesRegex(
            ValueError,
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            self.default_capacity_matrix,
            [[]],
        )

    def test_order_1(self):
        """Проверяет выброс исключения при передаче матрицы порядка 1"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.LESS_THAN_2_ERR_MSG}",
            MinCostFlowCalculator,
            [[1]],
            self.default_cost_matrix,
        )
        self.assertRaisesRegex(
            ValueError,
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.LESS_THAN_2_ERR_MSG}",
            MinCostFlowCalculator,
            self.default_capacity_matrix,
            [[1]],
        )

    def test_incorrect_values(self):
        """Проверяет выброс исключения при наличии некорректных значений в матрице"""
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            self.assertRaisesRegex(
                ValueError,
                f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
                MinCostFlowCalculator,
                [[0, value], [0, 0]],
                self.default_cost_matrix,
            )
            self.assertRaisesRegex(
                ValueError,
                f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
                MinCostFlowCalculator,
                self.default_capacity_matrix,
                [[0, value], [0, 0]],
            )

    def test_jag(self):
        """Проверяет выброс исключения при наличии строк разной длины в матрице."""
        jag_matrix = [[1, 2, 3], [1, 2]]
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            jag_matrix,
            self.default_cost_matrix,
        )
        self.assertRaisesRegex(
            ValueError,
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MinCostFlowCalculator,
            self.default_capacity_matrix,
            jag_matrix,
        )

    def test_negative_value(self):
        """Проверяет выброс исключения при наличии отрицательных значений в матрице"""
        incorrect_matrix = [[1, -1], [1, 2]]
        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(incorrect_matrix, self.default_cost_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            str(error.exception),
        )

        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(self.default_capacity_matrix, incorrect_matrix)
        self.assertEqual(
            f"{COST_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            str(error.exception),
        )

    def test_no_source(self):
        """Проверяет выброс исключения при отсутствии истока в сети"""
        incorrect_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [1, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(incorrect_matrix, incorrect_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SOURCE_ERR_MSG}",
            str(error.exception),
        )

    def test_2_source(self):
        """Проверяет выброс исключения при наличии нескольких истоков в сети"""
        incorrect_matrix = [
            # s a  t
            [0, 0, 0],  # s
            [0, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(incorrect_matrix, incorrect_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SOURCE_ERR_MSG}",
            str(error.exception),
        )

    def test_no_sink(self):
        """Проверяет выброс исключения при отсутствии стока в сети"""
        incorrect_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [0, 0, 3],  # a
            [0, 1, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(incorrect_matrix, incorrect_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SINK_ERR_MSG}",
            str(error.exception),
        )

    def test_2_sink(self):
        """Проверяет выброс исключения при наличии нескольких стоков в сети"""
        incorrect_matrix = [
            # s a  t
            [0, 2, 1],  # s
            [0, 0, 0],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MinCostFlowCalculator(incorrect_matrix, incorrect_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SINK_ERR_MSG}",
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
