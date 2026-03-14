import random as rnd
from dataclasses import dataclass

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

MUTATION_RATE = 0.1
"""Вероятность мутации особи."""

SELECTION_RATIO = 0.5
"""Доля особей, отбираемых для скрещивания."""

ELITE_RATIO = 0.2
"""Доля лучших особей (элита), гарантированно переходящих в следующее поколение."""


@dataclass
class PopulationStats:
    """Характеристики текущей популяции для отслеживания эволюционного прогресса."""

    generation: int
    size: int
    best_fitness: int
    avg_fitness: float
    worst_fitness: int
    best_chromosome: str

    def __str__(self):
        return (
            f"Поколение: {self.generation}, "
            f"Размер: {self.size}, "
            f"Лучший: {self.best_fitness}, "
            f"Средний: {self.avg_fitness:.2f}, "
            f"Худший: {self.worst_fitness}, "
            f"Хромосома лидера: {self.best_chromosome}"
        )


class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.

    Вариант 6: вывод характеристик каждого поколения (размер,средняя приспособленность, 
    лучший/худший результат и хромосома лидера),
    что позволяет многократно запускать алгоритм с небольшим количеством
    поколений и отслеживать эволюционный прогресс.
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
        self.__population_size = min(2**self.item_cnt // 2, POPULATION_LIMIT)
        self.__population = self.__generate_population(self.__population_size)
        self.__generation = 0
        self.__best_chromosome = max(self.__population, key=self.__population.get)
        self.__best_fitness = self.__population[self.__best_chromosome]

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        return [
            (self.__mask.format(chromosome), fitness)
            for chromosome, fitness in self.__population.items()
        ]

    @property
    def generation(self) -> int:
        """Возвращает номер текущего поколения."""
        return self.__generation

    def get_knapsack(self, epoch_cnt: int = EPOCH_CNT, verbose: bool = False) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма.

        Поддерживает многократный запуск: популяция и лучший найденный результат
        сохраняются между вызовами, результат никогда не ухудшается.

        :param epoch_cnt: количество поколений для выполнения алгоритма.
        :param verbose: если True, выводит характеристики каждого поколения.
        :return: KnapsackSolution с максимальной стоимостью и индексами предметов.
        """
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        for _ in range(epoch_cnt):
            self.__generation += 1

            parents = self.__select_parents()

            children = {}
            parent_keys = list(parents.keys())
            rnd.shuffle(parent_keys)
            for i in range(0, len(parent_keys) - 1, 2):
                first_child, second_child = self.__cross_items(parent_keys[i], parent_keys[i + 1])
                first_child = self.__mutation(first_child)
                second_child = self.__mutation(second_child)
                children[first_child] = self.__get_fit(first_child)
                children[second_child] = self.__get_fit(second_child)

            elite_size = max(2, int(self.__population_size * ELITE_RATIO))
            sorted_population = sorted(self.__population.items(), key=lambda x: x[1], reverse=True)
            next_population = dict(sorted_population[:elite_size])

            for chromosome, fitness in sorted(
                {**parents, **children}.items(), key=lambda x: x[1], reverse=True
            ):
                if len(next_population) >= self.__population_size:
                    break
                if chromosome not in next_population:
                    next_population[chromosome] = fitness

            if len(next_population) < self.__population_size:
                missing_count = int(self.__population_size) - len(next_population)
                next_population.update(self.__generate_population(missing_count))

            self.__population = next_population

            generation_best_chromosome = max(self.__population, key=self.__population.get)
            generation_best_fitness = self.__population[generation_best_chromosome]
            if generation_best_fitness > self.__best_fitness:
                self.__best_fitness = generation_best_fitness
                self.__best_chromosome = generation_best_chromosome

            if verbose:
                print(self.__collect_stats(self.__generation))

        selected_items = [bool(int(bit)) for bit in self.__mask.format(self.__best_chromosome)]
        best_items = [index for index, is_selected in enumerate(selected_items) if is_selected]
        return KnapsackSolution(cost=self.__best_fitness, items=best_items)

    def get_population_stats(self) -> PopulationStats:
        """Возвращает характеристики текущей популяции."""
        return self.__collect_stats(self.__generation)

    def __collect_stats(self, generation: int) -> PopulationStats:
        """Собирает и возвращает статистику текущей популяции."""
        all_fitness_values = list(self.__population.values())
        best_chromosome = max(self.__population, key=self.__population.get)
        return PopulationStats(
            generation=generation,
            size=len(self.__population),
            best_fitness=max(all_fitness_values),
            avg_fitness=sum(all_fitness_values) / len(all_fitness_values),
            worst_fitness=min(all_fitness_values),
            best_chromosome=self.__mask.format(best_chromosome),
        )

    def __select_parents(self) -> dict[int, int]:
        """Отбирает сильнейших особей для скрещивания (элитный отбор).

        Доля отбираемых особей определяется константой SELECTION_RATIO.
        Возвращает словарь особей с чётным количеством для парного скрещивания.
        """
        sorted_population = sorted(self.__population.items(), key=lambda x: x[1], reverse=True)
        parents_count = max(2, int(len(sorted_population) * SELECTION_RATIO))
        if parents_count % 2 != 0:
            parents_count += 1
        return dict(sorted_population[:parents_count])

    def __generate_population(self, population_size: int) -> dict[int, int]:
        """Генерирует популяцию случайным образом из жизнеспособных особей.

        :param population_size: требуемое количество особей в популяции.
        :return: словарь особей и их значений фитнес-функции.
        """
        population = {}
        max_chromosome_value = 2**self.item_cnt - 1
        for _ in range(int(population_size) * 50):
            if len(population) >= population_size:
                break
            candidate = rnd.randint(1, max_chromosome_value)
            candidate_fitness = self.__get_fit(candidate)
            if candidate_fitness > 0:
                population[candidate] = candidate_fitness
        if not population:
            population[0] = 0
        return population

    def __cross_items(self, ancestor1: int, ancestor2: int) -> tuple[int, int]:
        """Выполняет одноточечное скрещивание двух родительских особей.

        Точка разрыва хромосомы выбирается случайным образом. Первый потомок
        получает левую часть от первого родителя и правую от второго, второй —
        наоборот.

        :param ancestor1: первый родитель (целое число — кодировка хромосомы).
        :param ancestor2: второй родитель (целое число — кодировка хромосомы).
        :return: два потомка в виде целых чисел.
        """
        chromosome_length = self.item_cnt
        crossover_point = rnd.randint(1, chromosome_length - 1)
        right_mask = (1 << crossover_point) - 1
        left_mask = ((1 << chromosome_length) - 1) ^ right_mask
        first_child = (ancestor1 & left_mask) | (ancestor2 & right_mask)
        second_child = (ancestor2 & left_mask) | (ancestor1 & right_mask)
        return first_child, second_child

    def __mutation(self, chromosome: int) -> int:
        """Применяет мутацию к особи с вероятностью MUTATION_RATE.

        Мутация — инверсия одного случайного бита хромосомы.

        :param chromosome: особь (целое число — кодировка хромосомы).
        :return: особь после мутации.
        """
        if rnd.random() < MUTATION_RATE:
            mutation_position = rnd.randint(0, self.item_cnt - 1)
            chromosome ^= (1 << mutation_position)
        return chromosome

    def __get_fit(self, chromosome: int) -> int:
        """Вычисляет значение фитнес-функции для особи.

        :param chromosome: особь (целое число — кодировка хромосомы).
        :return: суммарная стоимость предметов, 0 если вес превышает ограничение.
        """
        selected_items = [bool(int(bit)) for bit in self.__mask.format(chromosome)]
        return self.get_cost(selected_items)