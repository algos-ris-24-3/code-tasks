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
            fitness_values = list(self.__population.values())
            keys = list(self.__population.keys())
            
            offspring = {}
            while len(offspring) < self.__population_cnt:
                parent1 = rnd.choices(keys, weights=fitness_values, k=1)[0]
                parent2 = rnd.choices(keys, weights=fitness_values, k=1)[0]
                child1, child2 = self.__cross_items(parent1, parent2)
                
                for child in (child1, child2):
                    if len(offspring) < self.__population_cnt:
                        mutated = self.__mutation(child)
                        fit = self.__get_fit(mutated)
                        if fit > 0:
                            offspring[mutated] = fit
            
            combined = {**self.__population, **offspring}
            
            sorted_items = sorted(combined.items(), key=lambda x: x[1], reverse=True)
            self.__population = dict(sorted_items[:self.__population_cnt])
        
        best_item_mask = max(self.__population, key=self.__population.get)
        item_idx = [i for i in range(self.item_cnt) if (best_item_mask >> (self.item_cnt - 1 - i)) & 1]
        return KnapsackSolution(self.__population[best_item_mask], item_idx)
    
    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """Генерирует начальную случайную популяцию."""
        population = {}
        while len(population) < population_cnt:
            item_mask = rnd.randint(0, (1 << self.item_cnt) - 1)
            while self.__get_fit(item_mask) == 0:
                ones_idx = [
                    i for i in range(self.item_cnt)
                    if (item_mask >> (self.item_cnt - 1 - i)) & 1
                ]
                if not ones_idx:
                    break
                idx_to_remove = rnd.choice(ones_idx)
                item_mask &= ~(1 << (self.item_cnt - 1 - idx_to_remove))
            fit_value = self.__get_fit(item_mask)
            if fit_value > 0:
                population[item_mask] = fit_value
            elif len(population) == 0 and item_mask == 0:
                population[0] = 0
        return population
    
    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Одноточечное скрещивание."""
        if self.item_cnt < 2:
            return ancestor1, ancestor2
        
        point = rnd.randint(1, self.item_cnt - 1)
        mask = (1 << (self.item_cnt - point)) - 1
        
        prefix1 = ancestor1 & ~mask
        suffix1 = ancestor1 & mask
        prefix2 = ancestor2 & ~mask
        suffix2 = ancestor2 & mask
        
        return (prefix1 | suffix2), (prefix2 | suffix1)

    def __mutation(self, item_set: int) -> int:
        """Мутация: инверсия случайного бита с вероятностью 10%."""
        if rnd.random() < 0.1:
            bit_pos = rnd.randint(0, self.item_cnt - 1)
            item_set ^= (1 << bit_pos)
        return item_set

    def __get_fit(self, item_mask: int) -> int:
        """Вычисляет значение фитнес-функции для заданного набора предметов."""
        total_weight = 0
        total_cost = 0
        for i in range(self.item_cnt):
            if (item_mask >> (self.item_cnt - 1 - i)) & 1:
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
