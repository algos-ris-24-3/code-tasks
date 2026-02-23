import unittest

from network_flow.error_message_enum import ErrorMessageEnum
from network_flow.max_flow_calculator import CAPACITY_MATRIX_NAME, MaxFlowCalculator


class TestMaxFlow(unittest.TestCase):
    """Набор тестов для проверки решения задачи о максимальном потоке."""

    def _check_max_flow(self, capacity_matrix, flow_matrix, expected_max_flow):
        """Проверяет корректность найденного максимального потока в сети"""
        self.assertEqual(
            len(capacity_matrix), len(flow_matrix), "Порядок матриц не совпадает"
        )
        order = len(capacity_matrix)

        for row_idx in range(order):
            self.assertEqual(
                order,
                len(capacity_matrix[row_idx]),
                f"Длина строки с индексом {row_idx} не совпадает с порядком матрицы пропускных способностей",
            )
            self.assertEqual(
                order,
                len(flow_matrix[row_idx]),
                f"Длина строки с индексом {row_idx} не совпадает с порядком матрицы потока",
            )

            for col_idx in range(order):
                self.assertGreaterEqual(
                    flow_matrix[row_idx][col_idx],
                    0,
                    f"локальный поток не может быть меньше нуля [{row_idx}][{col_idx}]",
                )
                self.assertLessEqual(
                    flow_matrix[row_idx][col_idx],
                    capacity_matrix[row_idx][col_idx],
                    f"локальный поток не может быть больше пропускной способности [{row_idx}][{col_idx}]",
                )

        vertices = MaxFlowCalculator.split_vertices_by_types(capacity_matrix)

        source_out_flow = 0
        for source_idx in vertices.sources:
            for col_idx in range(order):
                source_out_flow += flow_matrix[source_idx][col_idx]
        sink_in_flow = 0
        for sink_idx in vertices.sinks:
            for row_idx in range(order):
                sink_in_flow += flow_matrix[row_idx][sink_idx]

        self.assertEqual(
            source_out_flow, sink_in_flow, "Поток из истока не совпадает с потом в сток"
        )
        self.assertEqual(
            expected_max_flow,
            source_out_flow,
            "Величина потока не совпадает с ожидаемой",
        )

        for middle_idx in vertices.transits:
            flow_in = sum(
                [flow_matrix[row_idx][middle_idx] for row_idx in range(order)]
            )
            flow_out = sum(
                [flow_matrix[middle_idx][col_idx] for col_idx in range(order)]
            )
            self.assertEqual(
                flow_in, flow_out, "Поток, входящий в вершину не совпадает с исходящим"
            )

    def test_2_order(self):
        """Проверяет поиск максимального потока для сети из 2 вершин"""
        capacity_matrix = [
            # s  t
            [0, 1],  # s
            [0, 0],  # t
        ]
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(1, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_3_order(self):
        """Проверяет поиск максимального потока для сети из 3 вершин"""
        capacity_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [0, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(2, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_4_order(self):
        """Проверяет поиск максимального потока для сети из 3 вершин
        graph LR
        s-->|2|a
        s-->|1|b
        a-->|1|b
        a-->|1|t
        b-->|3|t
        """
        capacity_matrix = [
            # s a  b  t
            [0, 2, 1, 0],  # s
            [0, 0, 1, 1],  # a
            [0, 0, 0, 3],  # b
            [0, 0, 0, 0],  # t
        ]
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(3, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_5_order(self):
        """Проверяет поиск максимального потока для сети из 5 вершин
        graph LR
        s-->|7|a
        s-->|6|c
        a-->|3|b
        a-->|6|c
        a-->|3|t
        b-->|5|c
        b-->|2|t
        c-->|3|t
        """
        capacity_matrix = [
            # s a  b  c  t
            [0, 6, 0, 6, 0],  # s
            [0, 0, 3, 6, 3],  # a
            [0, 0, 0, 5, 2],  # b
            [0, 0, 0, 0, 3],  # c
            [0, 0, 0, 0, 0],  # t
        ]
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(8, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_6_order(self):
        """Проверяет поиск максимального потока для сети из 6 вершин
        graph LR
        s-->|3|a
        s-->|6|b
        a-->|2|b
        a-->|5|c
        b-->|4|c
        b-->|7|d
        c-->|8|d
        d-->|12|t
        """
        capacity_matrix = [
            # s a  b  c  d  t
            [0, 3, 6, 0, 0, 0],  # s
            [0, 0, 2, 5, 0, 0],  # a
            [0, 0, 0, 4, 7, 0],  # b
            [0, 0, 0, 0, 8, 0],  # c
            [0, 0, 0, 0, 0, 12],  # d
            [0, 0, 0, 0, 0, 0],  # t
        ]
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(9, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_6_order_with_loop(self):
        """Проверяет поиск максимального потока для сети из 3 вершин с циклом
        graph LR
        s-->|3|a
        s-->|6|b
        a-->|2|b
        c-->|5|a
        b-->|4|c
        b-->|7|d
        c-->|8|d
        d-->|12|t
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
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(8, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_10_order(self):
        """Проверяет поиск максимального потока для сети из 10 вершин
        graph LR
        s-->|7|a
        s-->|6|b
        s-->|5|c
        a-->|8|d
        b-->|5|e
        b-->|6|h
        c-->|3|b
        c-->|5|f
        d-->|4|b
        d-->|4|g
        e-->|8|t
        f-->|3|h
        f-->|3|t
        g-->|3|e
        g-->|3|t
        h-->|10|t
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
        result = MaxFlowCalculator(capacity_matrix)
        self.assertEqual(18, result.max_flow)
        self._check_max_flow(capacity_matrix, result.flow_matrix, result.max_flow)

    def test_none(self):
        """Проверяет выброс исключения при передаче `None` в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MaxFlowCalculator,
            None,
        )

    def test_empty(self):
        """Проверяет выброс исключения при передаче пустого списка в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MaxFlowCalculator,
            [],
        )

    def test_empty_row(self):
        """Проверяет выброс исключения при передаче списка с пустым списком в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MaxFlowCalculator,
            [[]],
        )

    def test_order_1(self):
        """Проверяет выброс исключения при передаче матрицы порядка 1"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.LESS_THAN_2_ERR_MSG}",
            MaxFlowCalculator,
            [[1]],
        )

    def test_incorrect_values(self):
        """Проверяет выброс исключения при наличии некорректных значений в матрице"""
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            self.assertRaisesRegex(
                ValueError,
                f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
                MaxFlowCalculator,
                [[0, value], [0, 0]],
            )

    def test_jag(self):
        """Проверяет выброс исключения при наличии строк разной длины в матрице."""
        matrix = [[1, 2, 3], [1, 2]]
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            MaxFlowCalculator,
            matrix,
        )

    def test_negative_value(self):
        """Проверяет выброс исключения при наличии отрицательных значений в матрице"""
        with self.assertRaises(ValueError) as error:
            MaxFlowCalculator([[1, -1], [1, 2]])
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            str(error.exception),
        )

    def test_no_source(self):
        """Проверяет выброс исключения при отсутствии истока в сети"""
        capacity_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [1, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MaxFlowCalculator(capacity_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SOURCE_ERR_MSG}",
            str(error.exception),
        )

    def test_2_source(self):
        """Проверяет выброс исключения при наличии нескольких истоков в сети"""
        capacity_matrix = [
            # s a  t
            [0, 0, 0],  # s
            [0, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MaxFlowCalculator(capacity_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SOURCE_ERR_MSG}",
            str(error.exception),
        )

    def test_no_sink(self):
        """Проверяет выброс исключения при отсутствии стока в сети"""
        capacity_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [0, 0, 3],  # a
            [0, 1, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MaxFlowCalculator(capacity_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SINK_ERR_MSG}",
            str(error.exception),
        )

    def test_2_sink(self):
        """Проверяет выброс исключения при наличии нескольких стоков в сети"""
        capacity_matrix = [
            # s a  t
            [0, 2, 1],  # s
            [0, 0, 0],  # a
            [0, 0, 0],  # t
        ]
        with self.assertRaises(ValueError) as error:
            MaxFlowCalculator(capacity_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SINK_ERR_MSG}",
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
