from network_flow.min_cost_flow_calculator import MinCostFlowCalculator
from network_flow.network_validator import NetworkValidator

SUPPLY_ERR_MSG = "Мощности заводов должны быть списком положительных целых чисел"
DEMAND_ERR_MSG = "Ёмкости складов должны быть списком положительных целых чисел"
COST_ERR_MSG = "Матрица стоимостей должна быть прямоугольной матрицей неотрицательных целых чисел размером N x K"
BALANCE_ERR_MSG = "Суммарная мощность заводов должна быть равна суммарной ёмкости складов"

TRANSPORT_COST_MATRIX_NAME = "Матрица стоимостей перевозки"


from collections import namedtuple

TransportationResult = namedtuple("TransportationResult", "transport_matrix min_cost")
"""
Результат решения транспортной задачи.

:ivar transport_matrix: Матрица перевозок, где transport_matrix[i][j] — количество единиц
                        продукции, перевозимых с i-го завода на j-й склад.
:type transport_matrix: list[list[int]]
:ivar min_cost: Минимальная суммарная стоимость всех перевозок.
:type min_cost: int
"""


class TransportationProblemSolver:
    """
    Класс для решения транспортной задачи методом сведения к задаче поиска
    максимального потока минимальной стоимости.

    """

    def __init__(
        self,
        supply: list[int],
        demand: list[int],
        cost_matrix: list[list[int]],
    ):
        """
        Конструктор класса.

        :param supply: cписок мощностей заводов. supply[i] — мощность i-го завода.
        :type supply: list[int]
        :param demand: cписок ёмкостей складов. demand[j] — ёмкость j-го склада.
        :type demand: list[int]
        :param cost_matrix: vатрица стоимостей перевозки размером N x K, где cost_matrix[i][j] — стоимость перевозки единицы
         продукции с i-го завода на j-й склад.
        :type cost_matrix: list[list[int]]
        :raises ValueError: tсли входные данные не соответствуют требованиям.
        """
        TransportationProblemSolver._validate_inputs(supply, demand, cost_matrix)

        self._supply = supply
        self._demand = demand
        self._cost_matrix = cost_matrix
        self._n_factories = len(supply)   
        self._n_warehouses = len(demand)  

        capacity_matrix, flow_cost_matrix = self._build_network()
        calculator = MinCostFlowCalculator(capacity_matrix, flow_cost_matrix)

        self._result = TransportationResult(
            transport_matrix=self._extract_transport_matrix(calculator.flow_matrix),
            min_cost=calculator.min_cost,
        )

    @property
    def result(self) -> TransportationResult:
        """Возвращает результат решения транспортной задачи."""
        return self._result

    def _build_network(self) -> tuple[list[list[int]], list[list[int]]]:
        """
        Строит сеть для задачи о максимальном потоке минимальной стоимости
        на основе данных транспортной задачи.

        :return: rортеж (capacity_matrix, cost_matrix) — матрица пропускных способностей
                 и матрица стоимостей для алгоритма MinCostFlowCalculator.
        :rtype: tuple[list[list[int]], list[list[int]]]
        """
        n = self._n_factories
        k = self._n_warehouses
        order = 1 + n + k + 1

        source_idx = 0
        sink_idx = order - 1
        factory_idx = lambda i: 1 + i
        warehouse_idx = lambda j: 1 + n + j

        capacity_matrix = [[0] * order for _ in range(order)]
        cost_matrix = [[0] * order for _ in range(order)]

        for i in range(n):
            capacity_matrix[source_idx][factory_idx(i)] = self._supply[i]

        for j in range(k):
            capacity_matrix[warehouse_idx(j)][sink_idx] = self._demand[j]

        for i in range(n):
            for j in range(k):
                capacity_matrix[factory_idx(i)][warehouse_idx(j)] = min(
                    self._supply[i], self._demand[j]
                )
                cost_matrix[factory_idx(i)][warehouse_idx(j)] = self._cost_matrix[i][j]

        return capacity_matrix, cost_matrix

    def _extract_transport_matrix(
        self, flow_matrix: tuple[tuple[int]]
    ) -> list[list[int]]:
        """
        Извлекает матрицу перевозок из матрицы локальных потоков сети.

        :param flow_matrix: матрица локальных потоков, полученная от MinCostFlowCalculator.
        :type flow_matrix: tuple[tuple[int]]
        :return: матрица перевозок размером N x K, где transport_matrix[i][j] —
                 количество единиц продукции, перевозимых с i-го завода на j-й склад.
        :rtype: list[list[int]]
        """
        n = self._n_factories
        k = self._n_warehouses

        factory_idx = lambda i: 1 + i
        warehouse_idx = lambda j: 1 + n + j

        transport_matrix = [[0] * k for _ in range(n)]
        for i in range(n):
            for j in range(k):
                transport_matrix[i][j] = flow_matrix[factory_idx(i)][warehouse_idx(j)]
        return transport_matrix

    @staticmethod
    def _validate_inputs(
        supply: list[int],
        demand: list[int],
        cost_matrix: list[list[int]],
    ) -> None:
        """
        Проверяет корректность входных данных транспортной задачи.

        :param supply: список мощностей заводов.
        :param demand: список ёмкостей складов.
        :param cost_matrix: матрица стоимостей перевозки.
        :raises ValueError: если входные данные не соответствуют требованиям.
        """
        if (
            not supply
            or not isinstance(supply, list)
            or not all(isinstance(a, int) and a > 0 for a in supply)
        ):
            raise ValueError(SUPPLY_ERR_MSG)

        if (
            not demand
            or not isinstance(demand, list)
            or not all(isinstance(b, int) and b > 0 for b in demand)
        ):
            raise ValueError(DEMAND_ERR_MSG)

        n = len(supply)
        k = len(demand)
        if (
            not cost_matrix
            or not isinstance(cost_matrix, list)
            or len(cost_matrix) != n
            or not all(
                isinstance(row, list)
                and len(row) == k
                and all(isinstance(c, int) and c >= 0 for c in row)
                for row in cost_matrix
            )
        ):
            raise ValueError(COST_ERR_MSG)

        if sum(supply) != sum(demand):
            raise ValueError(BALANCE_ERR_MSG)


if __name__ == "__main__":
    # Пример из лекции:
    # 3 завода с мощностями 5, 4, 3
    # 2 склада с ёмкостями 7, 5
    # Матрица стоимостей перевозки:
    #        Склад1  Склад2
    # Завод A:  30     20
    # Завод B:  25     15
    # Завод C:  40     50

    supply = [5, 4, 3]
    demand = [7, 5]
    cost_matrix = [
        [30, 20],
        [25, 15],
        [40, 50],
    ]

    print("Мощности заводов:", supply)
    print("Ёмкости складов:", demand)
    print("Матрица стоимостей перевозки:")
    for row in cost_matrix:
        print(" ", row)

    solver = TransportationProblemSolver(supply, demand, cost_matrix)
    result = solver.result

    print("\nМатрица перевозок (сколько единиц везём с завода i на склад j):")
    for row in result.transport_matrix:
        print(" ", row)
    print("Минимальная стоимость перевозок:", result.min_cost)