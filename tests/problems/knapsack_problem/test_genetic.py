import random as rnd
import unittest

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.genetic_solver import BRUTE_FORCE_BOUND, GeneticSolver
from tests.problems.knapsack_problem import check_knapsack_items
from tests.problems.knapsack_problem.test_abstract import TestAbstractSolver


class TestGeneticSolver(unittest.TestCase, TestAbstractSolver):
    """Набор тестов для проверки решения задачи о рюкзаке с использованием
    генетического алгоритма."""

    solver = GeneticSolver

    def test_simple(self):
        """Проверяет решение задачи на простом примере из 7 предметов."""
        weights = [10, 6, 11, 4, 1, 4, 3]
        costs = [15, 10, 22, 7, 1, 9, 4]
        weight_limit = 20
        result = self.solver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 39)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_random_simple(self):
        """Проверяет решение задачи на 20 случайных наборах небольшого размера.
        Полученный результат проверяется с помощью метода ветвей и границ.
        Тест ожидает, что на небольших размерах входных данных генетический
        алгоритм найдет правильный ответ не менее чем в 19 из 20.
        """
        right_answer_cnt = 0
        for _ in range(20):
            items_cnt = rnd.randint(BRUTE_FORCE_BOUND, BRUTE_FORCE_BOUND + 10)
            weights = [rnd.randint(1, 100) for _ in range(items_cnt)]
            costs = [rnd.randint(1, 100) for _ in range(items_cnt)]
            weight_limit = rnd.randint(min(weights), sum(weights))
            result = self.solver(weights, costs, weight_limit).get_knapsack()
            self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))
            bb_solver = BranchAndBoundSolver(weights, costs, weight_limit)
            if result.cost == bb_solver.get_knapsack().cost:
                right_answer_cnt += 1
        self.assertTrue(right_answer_cnt >= 19)

    def test_random_large(self):
        """Проверяет решение задачи на 20 случайных наборах большого размера
        (до 50 предметов).
        Полученный результат сравнивается со случайным набором предметов.
        Тест ожидает, что генетический алгоритм возвращает решение лучшее
         чем случайно выбранное не менее чем в 9 из 10.
        """
        better_than_random_answer_cnt = 0
        for _ in range(20):
            items_cnt = rnd.randint(BRUTE_FORCE_BOUND + 10, 50)
            weights = [rnd.randint(1, 100) for _ in range(items_cnt)]
            costs = [rnd.randint(1, 100) for _ in range(items_cnt)]
            weight_limit = rnd.randint(int(sum(weights) / 2), sum(weights))
            result = self.solver(weights, costs, weight_limit).get_knapsack()
            self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))
            random_set_cost = TestGeneticSolver.__get_random_set_cost(
                weights, costs, weight_limit
            )
            if result.cost > random_set_cost:
                better_than_random_answer_cnt += 1
        self.assertTrue(better_than_random_answer_cnt >= 19)

    def test_random_progress(self):
        """Проверяет прогресс улучшения результата при работе генетического
        алгоритма. Чем дольше работает алгоритм, тем лучший результат будет
        получен.
        Тест получает первый результат после 2 поколений алгоритма, затем 10
        раз запускает выполнение по 20 поколений.
        Тест ожидает, что при каждом следующем запуске полученный результат не
        ухудшается, а последний результат строго лучше первого.
        """
        items_cnt = 50
        weights = [rnd.randint(20, 80) for _ in range(items_cnt)]
        costs = [rnd.randint(20, 80) for _ in range(items_cnt)]
        weight_limit = int(sum(weights) * 0.66)
        gen_solver = self.solver(weights, costs, weight_limit)
        first_result = gen_solver.get_knapsack(2)
        last_result = None
        for _ in range(10):
            last_result = gen_solver.get_knapsack(20)
            self.assertTrue(last_result.cost >= first_result.cost)
        self.assertTrue(last_result.cost > first_result.cost)

    @staticmethod
    def __get_random_set_cost(weights, costs, weight_limit):
        """Генерирует случайный набор предметов, удовлетворяющий ограничению
        вместимости рюкзака, и возвращает его стоимость."""
        attempt = 0
        attempt_limit = 100
        mask = "{0:0" + str(len(weights)) + "b}"
        items_cnt = len(weights)
        item_set = rnd.randint(1, 2**items_cnt)
        set_str = mask.format(item_set)
        weight = sum(
            [weights[i] if bool(int(set_str[i])) else 0 for i in range(0, items_cnt)]
        )
        while weight > weight_limit and attempt < attempt_limit:
            item_set = rnd.randint(1, 2**items_cnt)
            set_str = mask.format(item_set)
            weight = sum(
                [
                    weights[i] if bool(int(set_str[i])) else 0
                    for i in range(0, items_cnt)
                ]
            )
            attempt += 1
        if weight > weight_limit:
            return 0
        return sum(
            [costs[i] if bool(int(set_str[i])) else 0 for i in range(0, items_cnt)]
        )


if __name__ == "__main__":
    unittest.main()
