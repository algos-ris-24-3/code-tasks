import unittest
from collections import namedtuple

from gcd_generator import GcdGenerator
from main import gcd_iterative_fast, gcd_iterative_slow, gcd_recursive, lcm

Case = namedtuple("Case", ["a", "b", "result"])


class TestGcd(unittest.TestCase):
    """Набор тестов для проверки реализации функций расчета НОД.
    Каждый тест запускается трижды, для каждой из реализаций расчета НОД"""

    gcd_functions = (gcd_recursive, gcd_iterative_slow, gcd_iterative_fast)
    simple_set = (
        Case(9, 3, 3),
        Case(-9, 3, 3),
        Case(3, 5, 1),
        Case(-18, -45, 9),
        Case(1, 0, 1),
        Case(0, 1, 1),
    )
    long_set = (
        Case(1005002, 1354, 2),
        Case(-1005002, 1354, 2),
        Case(65225655, 1610510, 805255),
        Case(-1944, -332024, 8),
        Case(65225655, 0, 65225655),
        Case(0, 65225655, 65225655),
    )

    def test_simple(self):
        """Проверка вычисления НОД на примерах небольших чисел"""
        for gcd in self.gcd_functions:
            for case in self.simple_set:
                self.assertEqual(case.result, gcd(case.a, case.b))

    def test_long(self):
        """Проверка вычисления НОД на примерах относительно больших чисел"""
        for gcd in self.gcd_functions:
            for case in self.long_set:
                self.assertEqual(case.result, gcd(case.a, case.b))

    @unittest.skipIf(
        GcdGenerator().gcd_value is None, "GcdGenerator is not implemented"
    )
    def test_random(self):
        """Проверка вычисления НОД на случайно сгенерированных примерах"""
        gcd_gen = GcdGenerator()
        for gcd in self.gcd_functions:
            for _ in range(10):
                if gcd == gcd_iterative_fast:
                    gcd_gen.generate_values(9, 5)
                else:
                    gcd_gen.generate_values(3, 2)
                self.assertEqual(
                    gcd(gcd_gen.a_value, gcd_gen.b_value), gcd_gen.gcd_value
                )


class TestLcm(unittest.TestCase):
    """Набор тестов для проверки реализации функции расчета НОК"""

    def test_primes(self):
        """Проверка вычисления НОК для простых чисел"""
        self.assertEqual(21, lcm(7, 3))

    def test_simple(self):
        """Проверка вычисления НОК для небольших чисел"""
        self.assertEqual(24, lcm(6, 8))

    def test_simple_long(self):
        """Проверка вычисления НОК для относительно больших чисел"""
        self.assertEqual(680386354, lcm(1005002, 1354))

    @unittest.skipIf(
        GcdGenerator().gcd_value is None, "GcdGenerator is not implemented"
    )
    def test_random(self):
        """Проверка вычисления НОК на случайно сгенерированных примерах"""
        gcd_gen = GcdGenerator()
        for _ in range(10):
            gcd_gen.generate_values()
            self.assertEqual(lcm(gcd_gen.a_value, gcd_gen.b_value), gcd_gen.lcm_value)


if __name__ == "__main__":
    unittest.main()
