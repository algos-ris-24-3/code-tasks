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
            return self._solve_by_brute_force()

        for _ in range(epoch_cnt):
            new_population = self._create_next_generation()
            self.__population = new_population

        return self._get_best_solution()

    def _solve_by_brute_force(self) -> KnapsackSolution:
        """Решает задачу полным перебором для маленьких входных данных."""
        brute_solver = BruteForceSolver(
            self.weights, self.costs, self.weight_limit
        )
        return brute_solver.get_knapsack()
    
    def _create_next_generation(self) -> dict[int, int]:
        """Создает новое поколение из текущей популяции."""
        best_item = max(self.__population, key=self.__population.get)
        new_population = {best_item: self.__population[best_item]}

        while len(new_population) < self.__population_cnt:
            child1, child2 = self._create_two_children()
            
            new_population[child1] = self.__get_fit(child1)
            if len(new_population) < self.__population_cnt:
                new_population[child2] = self.__get_fit(child2)

        return new_population
    
    def _create_two_children(self) -> tuple[int, int]:
        """Создает двух потомков от двух родителей."""
        ancestor1 = self._tournament_selection()
        ancestor2 = self._tournament_selection()

        child1, child2 = self.__cross_items(ancestor1, ancestor2)
        child1 = self.__mutation(child1)
        child2 = self.__mutation(child2)

        return child1, child2

    def _tournament_selection(self) -> int:
        """Турнирный отбор."""
        tourn_size = min(3, len(self.__population))
        participants = rnd.sample(list(self.__population.keys()), tourn_size)
        return max(participants, key=lambda x: self.__population[x])

    def _get_best_solution(self) -> KnapsackSolution:
        """Возвращает лучшее решение из текущей популяции."""
        best_item = max(self.__population, key=self.__population.get)
        best_cost = self.__population[best_item]
        selected_str = self.__mask.format(best_item)
        items = [idx for idx, bit in enumerate(selected_str) if bit == "1"]
        return KnapsackSolution(cost=best_cost, items=items)

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """Генерирует начальную популяцию случайных особей."""
        population = {}
        max_value = (1 << self.item_cnt) - 1
        while len(population) < population_cnt:
            item = rnd.randint(0, max_value)
            population[item] = self.__get_fit(item)
        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Двухточечное скрещивание"""
        if self.item_cnt < 2:
            return ancestor1, ancestor2

        str1 = self.__mask.format(ancestor1)
        str2 = self.__mask.format(ancestor2)

        cut1 = rnd.randint(0, self.item_cnt - 1)
        cut2 = rnd.randint(cut1 + 1, self.item_cnt)

        child1_str = str1[:cut1] + str2[cut1:cut2] + str1[cut2:]
        child2_str = str2[:cut1] + str1[cut1:cut2] + str2[cut2:]

        return int(child1_str, 2), int(child2_str, 2)

    def __mutation(self, item_set: int) -> int:
        """Мутация с вероятностью 5%."""
        if rnd.random() < 0.05:
            bit_pos = rnd.randint(0, self.item_cnt - 1)
            item_set ^= (1 << bit_pos)
        return item_set

    def __get_fit(self, item):
        """Вычисляет значение фитнес-функции для особи."""
        selected = [bool(int(char)) for char in self.__mask.format(item)]
        return self.get_cost(selected)


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
