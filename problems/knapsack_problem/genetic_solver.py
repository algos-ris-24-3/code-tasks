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

MUTATION_RATE = 0.02
"""Вероятность мутации одного гена особи."""

SELECTION_RATIO = 0.5
"""Доля особей, отбираемых для скрещивания."""

ELITE_RATIO = 0.1
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


# Хромосома — кортеж булевых значений (True/False для каждого предмета).
# Кортеж используется вместо списка чтобы хромосомы можно было хешировать
# и кешировать значения фитнес-функции, что значительно ускоряет алгоритм.
# Такое представление также позволяет работать с любым числом предметов
# без переполнения, которое возникает при хранении хромосомы как целого числа.
Chromosome = tuple[bool, ...]


class GeneticSolver(KnapsackAbstractSolver):
    """Класс для решения задачи о рюкзаке с использованием генетического
    алгоритма. Для входных данных небольшого размера используется полный перебор.

    Экземпляр класса хранит состояние популяции, метод поиска решения может
    быть запущен многократно для одного экземпляра.

    Вариант 6: предусмотрен вывод характеристик каждого поколения (размер,
    средняя приспособленность, лучший/худший результат и хромосома лидера),
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
        self.__population_size = min(2**self.item_cnt // 2, POPULATION_LIMIT)
        self.__fitness_cache: dict[Chromosome, int] = {}
        self.__fitness_cache_limit = POPULATION_LIMIT * 10
        self.__population = self.__generate_population(self.__population_size)
        self.__generation = 0
        self.__best_chromosome = max(self.__population, key=self.__get_fit)
        self.__best_fitness = self.__get_fit(self.__best_chromosome)

    @property
    def population(self) -> list[tuple[str, int]]:
        """Возвращает список особей текущей популяции. Для каждой особи
        возвращается строка из 0 и 1, а также значение фитнес-функции.
        """
        return [
            ("".join("1" if gene else "0" for gene in chromosome), self.__get_fit(chromosome))
            for chromosome in self.__population
        ]

    @property
    def generation(self) -> int:
        """Возвращает номер текущего поколения."""
        return self.__generation

    def get_knapsack(self, epoch_cnt: int = EPOCH_CNT, verbose: bool = False) -> KnapsackSolution:
        """Решает задачу о рюкзаке с использованием генетического алгоритма.

        Поддерживает многократный запуск: популяция и лучший найденный результат
        сохраняются между вызовами, результат никогда не ухудшается.

        :param epoch_cnt: Количество поколений для выполнения алгоритма.
        :param verbose: Если True, выводит характеристики каждого поколения.
        :return: KnapsackSolution с максимальной стоимостью и индексами предметов.
        """
        if self.item_cnt <= BRUTE_FORCE_BOUND:
            return BruteForceSolver(self.weights, self.costs, self.weight_limit).get_knapsack()

        for _ in range(epoch_cnt):
            self.__generation += 1
            parents = self.__select_parents()
            children = self.__produce_children(parents)
            self.__population = self.__form_next_population(parents, children)
            self.__update_best()
            if verbose:
                print(self.__collect_stats(self.__generation))

        return self.__build_solution()

    def get_population_stats(self) -> PopulationStats:
        """Возвращает характеристики текущей популяции."""
        return self.__collect_stats(self.__generation)

    def __produce_children(self, parents: list[Chromosome]) -> list[Chromosome]:
        """Создаёт потомков путём скрещивания и мутации родительских особей.

        :param parents: Список родительских хромосом.
        :return: Список хромосом потомков.
        """
        children = []
        shuffled_parents = parents[:]
        rnd.shuffle(shuffled_parents)
        for i in range(0, len(shuffled_parents) - 1, 2):
            first_child, second_child = self.__cross_items(
                shuffled_parents[i], shuffled_parents[i + 1]
            )
            children.append(self.__mutation(first_child))
            children.append(self.__mutation(second_child))
        return children

    def __form_next_population(
        self, parents: list[Chromosome], children: list[Chromosome]
    ) -> list[Chromosome]:
        """Формирует новое поколение популяции.

        Элита (лучшие особи текущего поколения) гарантированно переходит
        в следующее поколение. Оставшиеся места заполняются лучшими особями
        из родителей и потомков. При нехватке добавляются случайные особи.

        :param parents: Список родительских хромосом.
        :param children: Список хромосом потомков.
        :return: Список хромосом нового поколения.
        """
        elite_size = max(2, int(self.__population_size * ELITE_RATIO))
        sorted_population = sorted(self.__population, key=self.__get_fit, reverse=True)
        next_population = sorted_population[:elite_size]

        candidates = sorted(parents + children, key=self.__get_fit, reverse=True)
        for chromosome in candidates:
            if len(next_population) >= self.__population_size:
                break
            next_population.append(chromosome)

        if len(next_population) < self.__population_size:
            missing_count = self.__population_size - len(next_population)
            next_population.extend(self.__generate_population(missing_count))

        return next_population

    def __update_best(self) -> None:
        """Обновляет лучшее найденное решение за всё время работы алгоритма."""
        generation_best_chromosome = max(self.__population, key=self.__get_fit)
        generation_best_fitness = self.__get_fit(generation_best_chromosome)
        if generation_best_fitness > self.__best_fitness:
            self.__best_fitness = generation_best_fitness
            self.__best_chromosome = generation_best_chromosome

    def __build_solution(self) -> KnapsackSolution:
        """Формирует и возвращает итоговое решение на основе лучшей найденной хромосомы."""
        best_items = [
            index for index, is_selected in enumerate(self.__best_chromosome) if is_selected
        ]
        return KnapsackSolution(cost=self.__best_fitness, items=best_items)

    def __collect_stats(self, generation: int) -> PopulationStats:
        """Собирает и возвращает статистику текущей популяции."""
        all_fitness_values = [self.__get_fit(chromosome) for chromosome in self.__population]
        best_chromosome = max(self.__population, key=self.__get_fit)
        return PopulationStats(
            generation=generation,
            size=len(self.__population),
            best_fitness=max(all_fitness_values),
            avg_fitness=sum(all_fitness_values) / len(all_fitness_values),
            worst_fitness=min(all_fitness_values),
            best_chromosome="".join("1" if gene else "0" for gene in best_chromosome),
        )

    def __select_parents(self) -> list[Chromosome]:
        """Отбирает сильнейших особей для скрещивания (элитный отбор).

        Доля отбираемых особей определяется константой SELECTION_RATIO.
        Возвращает список с чётным количеством особей для парного скрещивания.
        """
        sorted_population = sorted(self.__population, key=self.__get_fit, reverse=True)
        parents_count = max(2, int(len(sorted_population) * SELECTION_RATIO))
        if parents_count % 2 != 0:
            parents_count += 1
        return sorted_population[:parents_count]

    def __generate_population(self, population_size: int) -> list[Chromosome]:
        """Генерирует популяцию из жизнеспособных особей.

        Хромосомы строятся жадно: предметы добавляются в случайном порядке
        до тех пор пока позволяет лимит веса. Это гарантирует что каждая
        сгенерированная особь сразу является допустимой, без перебора.

        :param population_size: Требуемое количество особей в популяции.
        :return: Список хромосом.
        """
        population = []
        item_indices = list(range(self.item_cnt))
        for _ in range(population_size):
            chromosome = [False] * self.item_cnt
            remaining_weight = self.weight_limit
            rnd.shuffle(item_indices)
            for index in item_indices:
                if self.weights[index] <= remaining_weight:
                    chromosome[index] = True
                    remaining_weight -= self.weights[index]
            population.append(tuple(chromosome))
        return population

    def __cross_items(
        self, first_parent: Chromosome, second_parent: Chromosome
    ) -> tuple[Chromosome, Chromosome]:
        """Выполняет одноточечное скрещивание двух родительских особей.

        Точка разрыва хромосомы выбирается случайным образом. Первый потомок
        получает левую часть от первого родителя и правую от второго, второй —
        наоборот.

        :param first_parent: Первый родитель.
        :param second_parent: Второй родитель.
        :return: Два потомка.
        """
        crossover_point = rnd.randint(1, self.item_cnt - 1)
        first_child = first_parent[:crossover_point] + second_parent[crossover_point:]
        second_child = second_parent[:crossover_point] + first_parent[crossover_point:]
        return first_child, second_child

    def __mutation(self, chromosome: Chromosome) -> Chromosome:
        """Применяет мутацию к особи.

        Выбирается фиксированное число позиций для инверсии на основе
        MUTATION_RATE, что быстрее чем проверка вероятности для каждого гена.

        :param chromosome: Исходная хромосома.
        :return: Хромосома после мутации.
        """
        mutations_count = max(1, int(self.item_cnt * MUTATION_RATE))
        mutation_positions = rnd.sample(range(self.item_cnt), mutations_count)
        mutable = list(chromosome)
        for position in mutation_positions:
            mutable[position] = not mutable[position]
        return tuple(mutable)

    def __get_fit(self, chromosome: Chromosome) -> int:
        """Вычисляет значение фитнес-функции для особи.

        Результат кешируется: повторный вызов с той же хромосомой возвращает
        сохранённое значение без пересчёта.

        :param chromosome: Хромосома особи.
        :return: Суммарная стоимость предметов, 0 если вес превышает ограничение.
        """
        if chromosome not in self.__fitness_cache:
            if len(self.__fitness_cache) >= self.__fitness_cache_limit:
                self.__fitness_cache.clear()
            self.__fitness_cache[chromosome] = self.get_cost(list(chromosome))
        return self.__fitness_cache[chromosome]