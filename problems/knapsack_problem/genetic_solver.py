import random as rnd

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 1000
"""Предельный размер популяции."""

EPOCH_CNT = 300
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
        """
        super().__init__(weights, costs, weight_limit)
        self.__mask = "{0:0" + str(len(weights)) + "b}"

        self.__population_cnt = min(POPULATION_LIMIT, max(60, self.item_cnt * 20))

        self.__ratio = sorted(
            range(self.item_cnt),
            key=lambda i: costs[i] / weights[i],
            reverse=True,
        )

        self.__fitness_cache = {}

        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции."""
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

            elite_cnt = max(1, self.__population_cnt // 15)

            for item, fit in sorted(
                population_items, key=lambda x: x[1], reverse=True
            )[:elite_cnt]:
                new_population[item] = fit

            pair_cnt = max(1, self.__population_cnt)

            for _ in range(pair_cnt):

                parent1 = self.__roulette_select(population_items, total_fit)
                parent2 = self.__roulette_select(population_items, total_fit)

                child1, child2 = self.__cross_items(parent1, parent2)

                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)

                child1 = self.__repair(child1)
                child2 = self.__repair(child2)

                child1 = self.__local_improve(child1)
                child2 = self.__local_improve(child2)

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
                    item = self.__repair(item)
                    item = self.__local_improve(item)

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

        seeds = [
            self.__greedy_ratio(),
            self.__greedy_cost(),
            self.__greedy_randomised(),
        ]

        for s in seeds:
            population[s] = self.__get_fit(s)

        while len(population) < population_cnt:
            item = rnd.getrandbits(self.item_cnt)
            item = self.__repair(item)
            item = self.__local_improve(item)
            population[item] = self.__get_fit(item)

        return population

    def __roulette_select(self, population_items, total_fit):
        """Выбор особи рулеткой."""
        if total_fit <= 0:
            return rnd.choice(population_items)[0]

        pick = rnd.uniform(0, total_fit)
        current = 0

        for item, fit in population_items:
            current += fit
            if current >= pick:
                return item

        return population_items[-1][0]

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Выполняет одноточечное скрещивание."""
        if self.item_cnt < 2:
            return ancestor1, ancestor2

        cross_point = rnd.randint(1, self.item_cnt - 1)
        mask = (1 << cross_point) - 1

        child1 = (ancestor1 & mask) | (ancestor2 & ~mask)
        child2 = (ancestor2 & mask) | (ancestor1 & ~mask)

        return child1, child2

    def __mutation(self, item_set: int) -> int:
        """Мутирует особь инверсией одного случайного бита."""
        if rnd.random() < 0.1:
            bit_pos = rnd.randrange(self.item_cnt)
            item_set ^= 1 << bit_pos
        return item_set

    def __repair(self, item: int) -> int:
        weight = 0
        chosen = []

        for i in range(self.item_cnt):
            if (item >> i) & 1:
                weight += self.weights[i]
                chosen.append(i)

        if weight <= self.weight_limit:
            return item

        chosen.sort(key=lambda i: self.costs[i] / self.weights[i])

        for i in chosen:
            item ^= 1 << i
            weight -= self.weights[i]
            if weight <= self.weight_limit:
                break

        return item

    def __local_improve(self, item: int) -> int:
        weight = sum(
            self.weights[i]
            for i in range(self.item_cnt)
            if (item >> i) & 1
        )

        for i in self.__ratio:
            if not ((item >> i) & 1):
                if weight + self.weights[i] <= self.weight_limit:
                    item |= 1 << i
                    weight += self.weights[i]

        return item

    def __greedy_ratio(self):
        w = 0
        item = 0
        for i in self.__ratio:
            if w + self.weights[i] <= self.weight_limit:
                item |= 1 << i
                w += self.weights[i]
        return item

    def __greedy_cost(self):
        order = sorted(range(self.item_cnt), key=lambda i: self.costs[i], reverse=True)
        w = 0
        item = 0
        for i in order:
            if w + self.weights[i] <= self.weight_limit:
                item |= 1 << i
                w += self.weights[i]
        return item

    def __greedy_randomised(self):
        w = 0
        item = 0
        order = self.__ratio[:]
        rnd.shuffle(order)
        for i in order:
            if w + self.weights[i] <= self.weight_limit:
                item |= 1 << i
                w += self.weights[i]
        return item

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