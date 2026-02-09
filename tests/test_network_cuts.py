import unittest

from network_flow.data_types import NetworkCutData
from network_flow.error_message_enum import ErrorMessageEnum
from network_flow.network_cuts_calculator import CAPACITY_MATRIX_NAME, NetworkCutsCalculator


class TestNetworkCuts(unittest.TestCase):
    """Набор тестов для проверки расчета пропускной способности разрезов сети."""

    def test_2_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 2"""
        capacity_matrix = [
            # s  t
            [0, 1],  # s
            [0, 0],  # t
        ]
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual([NetworkCutData(set([0]), set([1]), 1)], cuts)

    def test_3_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 3"""
        capacity_matrix = [
            # s a  t
            [0, 2, 0],  # s
            [0, 0, 3],  # a
            [0, 0, 0],  # t
        ]
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([2, 1]), 2),
                NetworkCutData(set([0, 1]), set([2]), 3),
            ],
            cuts,
        )

    def test_4_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 4
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
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([1, 2, 3]), 3),
                NetworkCutData(set([0, 1]), set([2, 3]), 3),
                NetworkCutData(set([0, 2]), set([1, 3]), 5),
                NetworkCutData(set([0, 1, 2]), set([3]), 4),
            ],
            cuts,
        )

    def test_5_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 5
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
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([1, 2, 3, 4]), 12),
                NetworkCutData(set([0, 1]), set([2, 3, 4]), 18),
                NetworkCutData(set([0, 2]), set([1, 3, 4]), 19),
                NetworkCutData(set([0, 3]), set([1, 2, 4]), 9),
                NetworkCutData(set([0, 1, 2]), set([3, 4]), 22),
                NetworkCutData(set([0, 1, 3]), set([2, 4]), 9),
                NetworkCutData(set([0, 2, 3]), set([1, 4]), 11),
                NetworkCutData(set([0, 1, 2, 3]), set([4]), 8),
            ],
            cuts,
        )

    def test_6_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 6
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
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([1, 2, 3, 4, 5]), 9),
                NetworkCutData(set([0, 1]), set([2, 3, 4, 5]), 13),
                NetworkCutData(set([0, 2]), set([1, 3, 4, 5]), 14),
                NetworkCutData(set([0, 3]), set([1, 2, 4, 5]), 17),
                NetworkCutData(set([0, 4]), set([1, 2, 3, 5]), 21),
                NetworkCutData(set([0, 1, 2]), set([3, 4, 5]), 16),
                NetworkCutData(set([0, 1, 3]), set([2, 4, 5]), 16),
                NetworkCutData(set([0, 1, 4]), set([2, 3, 5]), 25),
                NetworkCutData(set([0, 2, 3]), set([1, 4, 5]), 18),
                NetworkCutData(set([0, 2, 4]), set([1, 3, 5]), 19),
                NetworkCutData(set([0, 3, 4]), set([1, 2, 5]), 21),
                NetworkCutData(set([0, 1, 2, 3]), set([4, 5]), 15),
                NetworkCutData(set([0, 1, 2, 4]), set([3, 5]), 21),
                NetworkCutData(set([0, 1, 3, 4]), set([2, 5]), 20),
                NetworkCutData(set([0, 2, 3, 4]), set([1, 5]), 15),
                NetworkCutData(set([0, 1, 2, 3, 4]), set([5]), 12),
            ],
            cuts,
        )

    def test_6_order_with_loop(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 2 с циклом
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
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([1, 2, 3, 4, 5]), 9),
                NetworkCutData(set([0, 4]), set([1, 2, 3, 5]), 21),
                NetworkCutData(set([0, 3]), set([1, 2, 4, 5]), 22),
                NetworkCutData(set([0, 3, 4]), set([1, 2, 5]), 26),
                NetworkCutData(set([0, 2]), set([1, 3, 4, 5]), 14),
                NetworkCutData(set([0, 2, 4]), set([1, 3, 5]), 19),
                NetworkCutData(set([0, 2, 3]), set([1, 4, 5]), 23),
                NetworkCutData(set([0, 2, 3, 4]), set([1, 5]), 20),
                NetworkCutData(set([0, 1]), set([2, 3, 4, 5]), 8),
                NetworkCutData(set([0, 1, 4]), set([2, 3, 5]), 20),
                NetworkCutData(set([0, 1, 3]), set([2, 4, 5]), 16),
                NetworkCutData(set([0, 1, 3, 4]), set([2, 5]), 20),
                NetworkCutData(set([0, 1, 2]), set([3, 4, 5]), 11),
                NetworkCutData(set([0, 1, 2, 4]), set([3, 5]), 16),
                NetworkCutData(set([0, 1, 2, 3]), set([4, 5]), 15),
                NetworkCutData(set([0, 1, 2, 3, 4]), set([5]), 12),
            ],
            cuts,
        )

    def test_7_order(self):
        """Проверяет расчет пропускной способности разрезов для матрицы порядка 7
        graph LR
        s-->|7|a
        s-->|6|b
        s-->|5|c
        a-->|8|d
        b-->|5|e
        c-->|3|b
        d-->|4|b
        e-->|8|t
        """
        capacity_matrix = [
            # s a  b  c  d  e  t
            [0, 7, 6, 5, 0, 0, 0],  # s
            [0, 0, 0, 0, 8, 0, 0],  # a
            [0, 0, 0, 0, 0, 5, 0],  # b
            [0, 0, 3, 0, 0, 0, 0],  # c
            [0, 0, 4, 0, 0, 0, 0],  # d
            [0, 0, 0, 0, 0, 0, 8],  # e
            [0, 0, 0, 0, 0, 0, 0],  # t
        ]
        order = len(capacity_matrix)
        cuts = NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(2 ** (order - 2), len(cuts))
        self.assertCountEqual(
            [
                NetworkCutData(set([0]), set([1, 2, 3, 4, 5, 6]), 18),
                NetworkCutData(set([0, 5]), set([1, 2, 3, 4, 6]), 26),
                NetworkCutData(set([0, 4]), set([1, 2, 3, 5, 6]), 22),
                NetworkCutData(set([0, 4, 5]), set([1, 2, 3, 6]), 30),
                NetworkCutData(set([0, 3]), set([1, 2, 4, 5, 6]), 16),
                NetworkCutData(set([0, 3, 5]), set([1, 2, 4, 6]), 24),
                NetworkCutData(set([0, 3, 4]), set([1, 2, 5, 6]), 20),
                NetworkCutData(set([0, 3, 4, 5]), set([1, 2, 6]), 28),
                NetworkCutData(set([0, 2]), set([1, 3, 4, 5, 6]), 17),
                NetworkCutData(set([0, 2, 5]), set([1, 3, 4, 6]), 20),
                NetworkCutData(set([0, 2, 4]), set([1, 3, 5, 6]), 17),
                NetworkCutData(set([0, 2, 4, 5]), set([1, 3, 6]), 20),
                NetworkCutData(set([0, 2, 3]), set([1, 4, 5, 6]), 12),
                NetworkCutData(set([0, 2, 3, 5]), set([1, 4, 6]), 15),
                NetworkCutData(set([0, 2, 3, 4]), set([1, 5, 6]), 12),
                NetworkCutData(set([0, 2, 3, 4, 5]), set([1, 6]), 15),
                NetworkCutData(set([0, 1]), set([2, 3, 4, 5, 6]), 19),
                NetworkCutData(set([0, 1, 5]), set([2, 3, 4, 6]), 27),
                NetworkCutData(set([0, 1, 4]), set([2, 3, 5, 6]), 15),
                NetworkCutData(set([0, 1, 4, 5]), set([2, 3, 6]), 23),
                NetworkCutData(set([0, 1, 3]), set([2, 4, 5, 6]), 17),
                NetworkCutData(set([0, 1, 3, 5]), set([2, 4, 6]), 25),
                NetworkCutData(set([0, 1, 3, 4]), set([2, 5, 6]), 13),
                NetworkCutData(set([0, 1, 3, 4, 5]), set([2, 6]), 21),
                NetworkCutData(set([0, 1, 2]), set([3, 4, 5, 6]), 18),
                NetworkCutData(set([0, 1, 2, 5]), set([3, 4, 6]), 21),
                NetworkCutData(set([0, 1, 2, 4]), set([3, 5, 6]), 10),
                NetworkCutData(set([0, 1, 2, 4, 5]), set([3, 6]), 13),
                NetworkCutData(set([0, 1, 2, 3]), set([4, 5, 6]), 13),
                NetworkCutData(set([0, 1, 2, 3, 5]), set([4, 6]), 16),
                NetworkCutData(set([0, 1, 2, 3, 4]), set([5, 6]), 5),
                NetworkCutData(set([0, 1, 2, 3, 4, 5]), set([6]), 8),
            ],
            cuts,
        )

    def test_none(self):
        """Проверяет выброс исключения при передаче `None` в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            NetworkCutsCalculator.get_network_cuts,
            None,
        )

    def test_empty(self):
        """Проверяет выброс исключения при передаче пустого списка в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            NetworkCutsCalculator.get_network_cuts,
            [],
        )

    def test_empty_row(self):
        """Проверяет выброс исключения при передаче списка с пустым списком в качестве параметра"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            NetworkCutsCalculator.get_network_cuts,
            [[]],
        )

    def test_order_1(self):
        """Проверяет выброс исключения при передаче матрицы порядка 1"""
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.LESS_THAN_2_ERR_MSG}",
            NetworkCutsCalculator.get_network_cuts,
            [[1]],
        )

    def test_incorrect_values(self):
        """Проверяет выброс исключения при наличии некорректных значений в матрице"""
        incorrect_values = [None, "str", []]
        for value in incorrect_values:
            self.assertRaisesRegex(
                ValueError,
                f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
                NetworkCutsCalculator.get_network_cuts,
                [[0, value], [0, 0]],
            )

    def test_jag(self):
        """Проверяет выброс исключения при наличии строк разной длины в матрице."""
        matrix = [[1, 2, 3], [1, 2]]
        self.assertRaisesRegex(
            ValueError,
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.MATRIX_ERR_MSG}",
            NetworkCutsCalculator.get_network_cuts,
            matrix,
        )

    def test_negative_value(self):
        """Проверяет выброс исключения при наличии отрицательных значений в матрице"""
        with self.assertRaises(ValueError) as error:
            NetworkCutsCalculator.get_network_cuts([[1, -1], [1, 2]])
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
            NetworkCutsCalculator.get_network_cuts(capacity_matrix)
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
            NetworkCutsCalculator.get_network_cuts(capacity_matrix)
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
            NetworkCutsCalculator.get_network_cuts(capacity_matrix)
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
            NetworkCutsCalculator.get_network_cuts(capacity_matrix)
        self.assertEqual(
            f"{CAPACITY_MATRIX_NAME}: {ErrorMessageEnum.SINK_ERR_MSG}",
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
