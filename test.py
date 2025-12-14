import unittest

from main import (
    N_LESS_THAN_K_ERROR_MSG,
    NEGATIVE_VALUE_TEMPL,
    NOT_INT_VALUE_TEMPL,
    STR_LENGTH_ERROR_MSG,
    binomial_coefficient,
    generate_strings,
)
from strings_checker import check_strings


class TestZeroOne(unittest.TestCase):
    __incorrect_length_values = [None, 0, -1, 1.1, True, "string"]

    def test_incorrect_length_values(self):
        """Проверяет выброс исключения при некорректном значении параметра
        длина строки"""
        for incorrect_val in self.__incorrect_length_values:
            self.assertRaisesRegex(
                ValueError, STR_LENGTH_ERROR_MSG, generate_strings, incorrect_val
            )

    def test_zero_one(self):
        """Проверяет генерацию строк из 0 и 1 для длины строки от 1 до 20"""
        for target_string_length in range(1, 20):
            self.assertTrue(
                check_strings(
                    generate_strings(target_string_length), target_string_length
                )
            )


class TestBinomialCoefficient(unittest.TestCase):
    def test_n_less_than_k(self):
        """Проверяет выброс исключения при значении параметра n меньше чем k"""
        self.assertRaisesRegex(
            ValueError, N_LESS_THAN_K_ERROR_MSG, binomial_coefficient, 1, 2
        )

    def test_negative_n(self):
        """Проверяет выброс исключения при отрицательном значении параметра n"""
        self.assertRaisesRegex(
            ValueError, NEGATIVE_VALUE_TEMPL.format("n"), binomial_coefficient, -2, 2
        )

    def test_negative_k(self):
        """Проверяет выброс исключения при отрицательном значении параметра k"""
        self.assertRaisesRegex(
            ValueError, NEGATIVE_VALUE_TEMPL.format("k"), binomial_coefficient, 2, -2
        )

    def test_n_is_not_int(self):
        """Проверяет выброс исключения при нечисловом значении параметра n"""
        self.assertRaisesRegex(
            ValueError, NOT_INT_VALUE_TEMPL.format("n"), binomial_coefficient, "a", 2
        )

    def test_k_is_not_int(self):
        """Проверяет выброс исключения при нечисловом значении параметра k"""
        self.assertRaisesRegex(
            ValueError, NOT_INT_VALUE_TEMPL.format("k"), binomial_coefficient, 2, "b"
        )

    def test_binomial_coefficient_tiny(self):
        """Проверка вычисления биномиального коэффициента при небольших
        значениях параметров"""
        pascals_triangle = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        for n in range(len(pascals_triangle)):
            for k in range(len(pascals_triangle[n])):
                for use_rec in [True, False]:
                    res = binomial_coefficient(n, k, use_rec=use_rec)
                    self.assertEqual(res, pascals_triangle[n][k])

    def test_binomial_coefficient_middle(self):
        """Проверка вычисления биномиального коэффициента при средних
        значениях параметров"""
        for use_rec in [True, False]:
            res = binomial_coefficient(10, 5, use_rec=use_rec)
            self.assertEqual(res, 252)

    def test_binomial_coefficient_large(self):
        """Проверка вычисления биномиального коэффициента при больших
        значениях параметров"""
        for use_rec in [True, False]:
            res = binomial_coefficient(30, 20, use_rec=use_rec)
            self.assertEqual(res, 30045015)


if __name__ == "__main__":
    unittest.main()
