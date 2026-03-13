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
            return BruteForceSolver(self._weights, self._costs, self._weight_limit).get_knapsack()
        
        for epoch in range(epoch_cnt):
            generation = {}

            while len(generation) < self.__population_cnt:
                first_parent = self.tournament()
                second_parent = self.tournament()

                first_child, second_child = self.__cross_items(first_parent, second_parent)

                first_child = self.__mutation(first_child)
                second_child = self.__mutation(second_child)

                first_fitness = self.__get_fit(first_child)
                second_fitness = self.__get_fit(second_child)

                generation[first_child] = first_fitness

                if len(generation) < self.__population_cnt:
                    generation[second_child] = second_fitness

            elite = 0

            elite_fitness = -1

            for possible_elite, fitness in self.__population.items():
                if fitness > elite_fitness:
                    elite_fitness = fitness

                    elite = possible_elite

            if elite not in generation or generation[elite] < elite_fitness:
                generation[elite] = elite_fitness

            self.__population = generation

        best_solution = 0

        best_fitness = -1

        for possible, fit in self.__population.items():
            if fit > best_fitness:
                best_fitness = fit

                best_solution = possible

        if best_fitness <= 0:
            return KnapsackSolution(0, [])    

        bin_view = self.__mask.format(best_solution)

        taken = [index for index, digit in enumerate(bin_view) if digit == '1']

        return KnapsackSolution(best_fitness, taken)    

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        population = {}

        while len(population) < population_cnt:
            possible = rnd.randint(0, 2**self.item_cnt - 1)

            if possible not in population:
                population[possible] = self.__get_fit(possible)

        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        first_bin = self.__mask.format(ancestor1)
        second_bin = self.__mask.format(ancestor2)

        first_dot = rnd.randint(0, self.item_cnt - 1)
        second_dot = rnd.randint(first_dot, self.item_cnt)

        first_child = first_bin[:first_dot] + second_bin[first_dot:second_dot] + first_bin[second_dot:]
        second_child = second_bin[:first_dot] + first_bin[first_dot:second_dot] + second_bin[second_dot:]

        return int(first_child, 2), int(second_child, 2)

    def __mutation(self, item_set: int) -> int:
        for index in range(self.item_cnt):
            if rnd.random() < 0.01:
                item_set ^= (1 << index)

        return item_set

    def __get_fit(self, item):
        bin_view = self.__mask.format(item)

        is_taken = []

        for digit in bin_view:
            if digit == '1':
                is_taken.append(True)
            else:
                is_taken.append(False)

        return self.get_cost(is_taken)

    def tournament(self):
        individual_amount = 2

        possible = list(self.__population.keys())

        participants = rnd.sample(possible, min(individual_amount, len(possible)))

        winner = 0

        winner_fitness = -1

        for participant in participants:
            fitness = self.__population[participant]

            if fitness > winner_fitness:
                winner_fitness = fitness

                winner = participant

        return winner


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
