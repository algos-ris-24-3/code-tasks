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
        self.__population_cnt = min(2**self.item_cnt / 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_cnt)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        population_data = []
        for key in self.__population.keys():
            population_data.append((self.__mask.format(key), self.__population[key]))
        return population_data

    def get_knapsack(self, epoch_cnt=EPOCH_CNT) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма."""
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        for _ in range(epoch_cnt):

            sorted_population = sorted(
                self.__population.items(), key=lambda x: x[1], reverse=True
            )
            selection_cnt = max(2, len(sorted_population) // 3)
            selected = [item[0] for item in sorted_population[:selection_cnt]]

            offspring = []
            for i in range(0, len(selected) - 1, 2):
                child1, child2 = self.__cross_items(selected[i], selected[i + 1])
                offspring.append(child1)
                offspring.append(child2)

            if len(selected) % 2 != 0:
                child1, child2 = self.__cross_items(selected[-1], selected[0])
                offspring.append(child1)
                offspring.append(child2)

            offspring = [self.__mutation(child) for child in offspring]

            elite = [item[0] for item in sorted_population[:2]]

            new_population_keys = list(dict.fromkeys(elite + offspring))

            while len(new_population_keys) < self.__population_cnt:
                random_item = rnd.randint(0, 2**self.item_cnt - 1)
                if random_item not in new_population_keys:
                    
                    new_population_keys.append(random_item)

            self.__population = {
                key: self.__get_fit(key) for key in new_population_keys
            }

        best_chromosome = max(self.__population, key=lambda x: self.__population[x])
        best_fit = self.__population[best_chromosome]

        items = []
        for i in range(self.item_cnt):

            if best_chromosome & (1 << (self.item_cnt - 1 - i)):
                items.append(i)

        return KnapsackSolution(cost=best_fit, items=items)





    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        population = {}
        max_chromosome = 2**self.item_cnt - 1
        attempts = 0
        max_attempts = population_cnt * 10

        while len(population) < population_cnt and attempts < max_attempts:
            chromosome = rnd.randint(0, max_chromosome)
            if chromosome not in population:
                population[chromosome] = self.__get_fit(chromosome)
            attempts += 1

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        child1 = 0
        child2 = 0
        for i in range(self.item_cnt):


            bit_mask = 1 << i
            if rnd.random() < 0.5:
                child1 |= ancestor1 & bit_mask
                child2 |= ancestor2 & bit_mask
            else:
                child1 |= ancestor2 & bit_mask
                child2 |= ancestor1 & bit_mask
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        bit_idx = rnd.randint(0, self.item_cnt - 1)
        mutated = item_set ^ (1 << bit_idx)

        if self.__get_fit(mutated) == 0 or mutated == item_set:
            return item_set
        return mutated

    def __get_fit(self, item):
        total_weight = 0
        total_cost = 0
        for i in range(self.item_cnt):

            if item & (1 << (self.item_cnt - 1 - i)):
                total_weight += self.weights[i]
                total_cost += self.costs[i]

        if total_weight > self.weight_limit:
            return 0
        return total_cost


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
        f"Максимальная стоимость: {result.cost}, " f"индексы предметов: {result.items}"
    )
