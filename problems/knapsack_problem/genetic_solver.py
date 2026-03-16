import random as rnd

from problems.knapsack_problem.bb_solver import BranchAndBoundSolver
from problems.knapsack_problem.brute_force_solver import BruteForceSolver
from problems.knapsack_problem.knapsack_abs_solver import (
    KnapsackAbstractSolver,
    KnapsackSolution,
)

POPULATION_LIMIT = 500
"""Предельный размер популяции."""

EPOCH_CNT = 500
"""Количество поколений по умолчанию."""

BRUTE_FORCE_BOUND = 5
"""Размер входных данных задачи, до которого используется полный перебор."""

ELITE_RATIO = 0.1
"""Доля лучших особей, сохраняемых между поколениями (элитизм)."""


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
        self.__elite_cnt = max(2, int(self.__population_cnt * ELITE_RATIO))
        self.__population = self.__generate_population(self.__population_cnt)
        self.__best_solution = None
        self.__best_fitness = 0

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
        """Решает задачу о рюкзаке с использованием генетического алгоритма.
        """
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            solver = BruteForceSolver(self.weights, self.costs, self.weight_limit)
            return solver.get_knapsack()
        
        self.__update_best_solution()
        
        for _ in range(epoch_cnt):
            total_fitness = sum(self.__population.values())
            
            if total_fitness == 0:
                self.__population = self.__generate_population(self.__population_cnt)
                continue
            
            elite = self.__get_elite()
            
            new_population = dict(elite)
            
            while len(new_population) < self.__population_cnt:
                parent1 = self.__roulette_selection(total_fitness)
                parent2 = self.__roulette_selection(total_fitness)
                
                child1, child2 = self.__cross_items(parent1, parent2)
                
                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)
                
                if child1 not in new_population:
                    new_population[child1] = self.__get_fit(child1)
                if child2 not in new_population and len(new_population) < self.__population_cnt:
                    new_population[child2] = self.__get_fit(child2)
            
            self.__population = new_population
            
            self.__update_best_solution()
        
        return self.__create_solution(self.__best_solution, self.__best_fitness)

    def __update_best_solution(self) -> None:
        """Обновляет лучшее найденное решение на основе текущей популяции."""
        for item, fitness in self.__population.items():
            if fitness > self.__best_fitness:
                self.__best_fitness = fitness
                self.__best_solution = item
    
    def __get_elite(self) -> dict[int, int]:
        """Возвращает лучших по фитнесу особей."""
        sorted_population = sorted(
            self.__population.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return dict(sorted_population[:self.__elite_cnt])
    
    def __create_solution(self, item: int, cost: int) -> KnapsackSolution:
        """Создает объект решения из битовой маски."""
        items = []
        if item is not None:
            binary_str = self.__mask.format(item)
            for i, bit in enumerate(binary_str):
                if bit == '1':
                    items.append(i)
        return KnapsackSolution(cost, items)

    def __roulette_selection(self, total_fitness: int) -> int:
        """Выбор особи методом рулетки."""
        pick = rnd.uniform(0, total_fitness)
        current = 0
        for item, fitness in self.__population.items():
            current += fitness
            if current >= pick:
                return item
        return list(self.__population.keys())[-1]

    def __generate_population(self, population_cnt: int) -> dict[int:int]:
        """Генерирует начальную популяцию случайных особей."""
        population = {}
        max_value = 2 ** self.item_cnt
        
        while len(population) < population_cnt:
            item = rnd.randint(0, max_value - 1)
            if item not in population:
                population[item] = self.__get_fit(item)
        
        return population

    def __cross_items(self, parent1: int, parent2: int) -> tuple[int, int]:
        """Одноточечное скрещивание двух особей."""
        if self.item_cnt <= 1:
            return parent1, parent2
        
        crossover_point = rnd.randint(1, self.item_cnt - 1)
        
        right_mask = (1 << crossover_point) - 1
        left_mask = ((1 << self.item_cnt) - 1) ^ right_mask
        
        child1 = (parent1 & left_mask) | (parent2 & right_mask)
        child2 = (parent2 & left_mask) | (parent1 & right_mask)
        
        return child1, child2

    def __mutation(self, item_set: int) -> int:
        """Мутация особи - инвертирование случайного бита с небольшой вероятностью."""
        mutation_rate = 1.0 / self.item_cnt
        
        for i in range(self.item_cnt):
            if rnd.random() < mutation_rate:
                item_set ^= (1 << i)
        
        return item_set

    def __get_fit(self, item: int) -> int:
        """Вычисляет значение фитнес-функции для особи."""
        total_weight = 0
        total_cost = 0
        
        for i in range(self.item_cnt):
            if item & (1 << (self.item_cnt - 1 - i)):
                total_weight += self.weights[i]
                total_cost += self.costs[i]
        
        if total_weight <= self.weight_limit:
            return total_cost
        return 0


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
