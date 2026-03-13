import random as rnd
import time

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

    def get_knapsack(self, epoch_cnt=EPOCH_CNT, time_limit_sec: float | None = None) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма.

        Остановка алгоритма выполняется по числу поколений (epoch_cnt). Дополнительно
        может быть задано ограничение по времени (time_limit_sec, в секундах).
        """
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        if epoch_cnt is None:
            epoch_cnt = EPOCH_CNT
        epoch_cnt = int(epoch_cnt)
        if epoch_cnt <= 0:
            return KnapsackSolution(cost=0, items=[])

        if time_limit_sec is not None:
            time_limit_sec = float(time_limit_sec)
            if time_limit_sec <= 0:
                time_limit_sec = 0.0

        start = time.perf_counter()
        deadline = None if time_limit_sec is None else start + time_limit_sec

        def time_exceeded() -> bool:
            return deadline is not None and time.perf_counter() >= deadline

        if not getattr(self, "_GeneticSolver__population", None):
            self.__population = self.__generate_population(self.__population_cnt)

        best_genome = "0" * self.item_cnt
        best_fit = 0

        mutation_prob = 0.1

        for _ in range(epoch_cnt):
            if time_exceeded():
                break

            if not self.__population:
                self.__population = self.__generate_population(self.__population_cnt)

            for genome, fit in self.__population.items():
                if fit > best_fit:
                    best_fit = fit
                    best_genome = genome

            ranked = sorted(self.__population.items(), key=lambda x: x[1], reverse=True)
            parents = [genome for genome, _ in ranked[: max(1, len(ranked) // 2)]]

            if ranked[0][1] == 0:
                self.__population = self.__generate_population(self.__population_cnt)
                continue

            next_population: dict[str, int] = {}

            elite_cnt = max(1, len(parents) // 4)
            for genome, fit in ranked[:elite_cnt]:
                next_population[genome] = fit

            while len(next_population) < self.__population_cnt and not time_exceeded():
                parent1 = rnd.choice(parents)
                parent2 = rnd.choice(parents)
                child1, child2 = self.__cross_items(parent1, parent2)

                if rnd.random() < mutation_prob:
                    child1 = self.__mutation(child1)
                if rnd.random() < mutation_prob:
                    child2 = self.__mutation(child2)

                next_population[child1] = self.__get_fit(child1)
                if len(next_population) < self.__population_cnt:
                    next_population[child2] = self.__get_fit(child2)

            self.__population = next_population

        selected_bits = [c == "1" for c in best_genome]
        return KnapsackSolution(
            cost=best_fit,
            items=[idx for idx, is_selected in enumerate(selected_bits) if is_selected],
        )

    def __generate_population(self, population_cnt: int) -> dict[str, int]:
        population_cnt = int(population_cnt)
        population_cnt = max(1, population_cnt)

        population: dict[str, int] = {}
        while len(population) < population_cnt:
            genome = "".join(rnd.choice("01") for _ in range(self.item_cnt))
            population[genome] = self.__get_fit(genome)
        return population

    def __cross_items(self, ancestor1: str, ancestor2: str) -> tuple[str, str]:
        if self.item_cnt <= 1:
            return ancestor1, ancestor2
        point = rnd.randint(1, self.item_cnt - 1)
        child1 = ancestor1[:point] + ancestor2[point:]
        child2 = ancestor2[:point] + ancestor1[point:]
        return child1, child2

    def __mutation(self, item_set: str) -> str:
        if self.item_cnt == 0:
            return item_set
        idx = rnd.randrange(0, self.item_cnt)
        new_bit = "1" if item_set[idx] == "0" else "0"
        return item_set[:idx] + new_bit + item_set[idx + 1 :]

    def __get_fit(self, item: str) -> int:
        selected = [c == "1" for c in item]
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
