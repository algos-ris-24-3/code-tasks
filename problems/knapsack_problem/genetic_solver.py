import random as rnd

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 1000
"""Предельный размер популяции."""

EPOCH_CNT = 100
"""Количество поколений по умолчанию."""

BRUTE_FORCE_BOUND = 5
"""Размер входных данных задачи, до которого используется полный перебор."""


class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный
    перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.
    """

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создает объект класса для решения задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"
        self.__population_cnt = int(min(2**self.item_cnt / 2, POPULATION_LIMIT))
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        return [
            (self.__mask.format(item), fit)
            for item, fit in self.__population.items()
        ]

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(
                self.weights, self.costs, self.weight_limit
            ).get_knapsack()

        best_item = max(self.__population, key=self.__population.get)
        best_fit = self.__population[best_item]

        for _ in range(epoch_cnt):
            population_items = list(self.__population.items())
            total_fit = sum(fit for _, fit in population_items)

            new_population = {}

            elite_cnt = max(1, self.__population_cnt // 20)

            for item, fit in sorted(
                population_items, key=lambda x: x[1], reverse=True
            )[:elite_cnt]:
                new_population[item] = fit

            pair_cnt = self.__population_cnt

            for _ in range(pair_cnt):
                parent1 = self.__roulette_select(population_items, total_fit)
                parent2 = self.__roulette_select(population_items, total_fit)

                child1, child2 = self.__cross_items(parent1, parent2)
                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)

                if child1 not in new_population:
                    new_population[child1] = self.__get_fit(child1)

                if (
                    len(new_population) < self.__population_cnt
                    and child2 not in new_population
                ):
                    new_population[child2] = self.__get_fit(child2)

                if len(new_population) >= self.__population_cnt:
                    break

            

            if len(new_population) < self.__population_cnt:
                for item, fit in sorted(
                    self.__population.items(), key=lambda x: x[1], reverse=True
                ):
                    if item not in new_population:
                        new_population[item] = fit
                    if len(new_population) >= self.__population_cnt:
                        break

            if len(new_population) < self.__population_cnt:
                attempts = 0
                max_attempts = self.__population_cnt * 20

                while (
                    len(new_population) < self.__population_cnt
                    and attempts < max_attempts
                ):
                    item = rnd.getrandbits(self.item_cnt)
                    if item not in new_population:
                        new_population[item] = self.__get_fit(item)
                    attempts += 1

            self.__population = new_population

            current_best = max(self.__population, key=self.__population.get)
            current_best_fit = self.__population[current_best]
            if current_best_fit > best_fit:
                best_item = current_best
                best_fit = current_best_fit

        best_bits = self.__mask.format(best_item)
        best_items = [idx for idx, bit in enumerate(best_bits) if bit == "1"]

        return KnapsackSolution(cost=best_fit, items=best_items)

    def __generate_population(self, population_cnt: int) -> dict[int, int]:
        """Генерирует начальную популяцию."""
        population = {}
        max_unique_cnt = min(population_cnt, 2**self.item_cnt)

        while len(population) < max_unique_cnt:
            item = rnd.getrandbits(self.item_cnt)
            population[item] = self.__get_fit(item)

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Выполняет одноточечное скрещивание."""
        if self.item_cnt < 2:
            return ancestor1, ancestor2

        bits1 = self.__mask.format(ancestor1)
        bits2 = self.__mask.format(ancestor2)

        cross_point = rnd.randint(1, self.item_cnt - 1)

        child1_bits = bits1[:cross_point] + bits2[cross_point:]
        child2_bits = bits2[:cross_point] + bits1[cross_point:]

        return int(child1_bits, 2), int(child2_bits, 2)
    
    def __roulette_select(self, population_items, total_fit):

        if total_fit == 0:
            return rnd.choice(population_items)[0]

        pick = rnd.uniform(0, total_fit)
        current = 0

        for item, fit in population_items:
            current += fit
            if current >= pick:
                return item

    def __mutation(self, item_set: int) -> int:
        """Мутирует особь инверсией одного случайного бита."""

        if rnd.random() < 2 / self.item_cnt:
            bit_pos = rnd.randint(0, self.item_cnt - 1)
            item_set ^= 1 << (self.item_cnt - 1 - bit_pos)

        return item_set

    def __get_fit(self, item):
        """Возвращает значение фитнес-функции для особи."""
        if item in self.__fitness_cache:
            return self.__fitness_cache[item]

        selected_items = [
            bit == "1"
            for bit in self.__mask.format(item)
        ]

        fit = self.get_cost(selected_items)

        self.__fitness_cache[item] = fit
        return fit


if __name__ == "__main__":
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30

    print("Пример решения задачи о рюкзаке\n")
    print(f"Веса предметов для комплектования рюкзака: {weights}")
    print(f"Стоимости предметов для комплектования рюкзака: {costs}")
    print(f"Ограничение вместимости рюкзака: {weight_limit}")

    solver = GeneticSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()

    print(
        f"Максимальная стоимость: {result.cost}, индексы предметов: {result.items}"
    )
