from math import inf

from network_flow.max_flow_calculator import MaxFlowCalculator
from network_flow.network_validator import NetworkValidator
from shortest_path.bellman_ford import (
    NegativeLoopBellmanFordError,
    bellman_ford,
    restore_path,
)
from shortest_path.floyd_warshall import NegativeLoopFloydWarshallError, floyd_warshall

COST_MATRIX_NAME = "Таблица стоимости транспортировки"


class MinCostFlowCalculator(MaxFlowCalculator):
    """Класс для решения задачи поиска максимального потока минимальной стоимости"""

    def __init__(self, capacity_matrix: list[list[int]], cost_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        :param cost_matrix: Квадратная матрица стоимости транспортировки.
        :type cost_matrix: list[list[int]]
        """
        NetworkValidator.validate_matrix(cost_matrix, COST_MATRIX_NAME)
        # Максимальный поток рассчитывается в родительском классе,
        # сохраняется значением максимального потока и матрица локальных потоков
        super().__init__(capacity_matrix)

        self._cost_matrix = cost_matrix
        self._residual_matrix, self._cost_residual_matrix = (
            self._get_residual_matrices()
        )
        self._minimize_cost()
        self._min_cost = self._get_cost_by_flow()

    @property
    def min_cost(self) -> int:
        """Возвращает минимальную стоимость потока"""
        return self._min_cost

    def _minimize_cost(self) -> None:
        """Осуществляет минимизацию стоимости максимального потока
        посредством поиска и удаления отрицательных циклов в остаточной сети.
        После удаления всех циклов обновляет матрицу локальных потоков
        на основе остаточной сети."""
        while True:
            loop = self._find_negative_loop()
            if not loop:
                break
            self._remove_negative_loop(loop)

        self._update_flow_matrix()

    def _find_negative_loop(self) -> list[int]:
        """Возвращает найденный цикл отрицательной стоимости в остаточной сети
        стоимости транспортировки. Возвращает пустой список, если цикл не найден."""
        distances = [0] * self._order
        predecessors = [None] * self._order

        edges = []
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if self._residual_matrix[row_idx][col_idx] > 0:
                    edges.append((row_idx, col_idx, self._cost_residual_matrix[row_idx][col_idx]))

        last_updated_vertex = None
        for i in range(self._order):
            last_updated_vertex = None
            for row_idx, col_idx, weight in edges:
                if distances[row_idx] + weight < distances[col_idx]:
                    distances[col_idx] = distances[row_idx] + weight
                    predecessors[col_idx] = row_idx
                    last_updated_vertex = col_idx

        if last_updated_vertex is None:
            return []

        curr = last_updated_vertex
        for _ in range(self._order):
            curr = predecessors[curr]

        cycle = []
        col_idx = curr
        while True:
            cycle.append(col_idx)
            if col_idx == curr and len(cycle) > 1:
                break
            col_idx = predecessors[col_idx]

        return cycle[::-1]

    def _remove_negative_loop(self, loop: list[int]) -> None:
        """Удаляет цикл отрицательной стоимости в остаточных сетях потоков и стоимостей."""
        delta = inf
        for i in range(len(loop) - 1):
            row_idx, col_idx = loop[i], loop[i + 1]
            delta = min(delta, self._residual_matrix[row_idx][col_idx])

        for i in range(len(loop) - 1):
            row_idx, col_idx = loop[i], loop[i + 1]
            self._residual_matrix[row_idx][col_idx] -= delta
            self._residual_matrix[col_idx][row_idx] += delta

    def _update_flow_matrix(self):
        """Обновляет матрицу локальных потоков на основе остаточной сети.
        В остаточной сети MinCostFlowCalculator (созданной в _get_residual_matrices):
        - residual_matrix[row_idx][col_idx] - остаточная способность (reserve)
        - residual_matrix[col_idx][row_idx] - текущий поток (flow)
        """
        flow_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if self._capacity_matrix[row_idx][col_idx] > 0:
                    flow_matrix[row_idx][col_idx] = self._residual_matrix[col_idx][row_idx]
        self._flow_matrix = flow_matrix

    def _get_residual_matrices(self):
        """Возвращает остаточные сети, созданные на основе матриц
        локальных потоков и пропускных способностей:
        - residual_matrix - остаточная сеть с указанием потоков и резервов.
        - cost_residual_matrix - остаточная сеть с указанием стоимости транспортировки.
        """
        residual_matrix = [[0] * self._order for _ in range(self._order)]
        cost_residual_matrix = [[0] * self._order for _ in range(self._order)]

        for row_idx in range(self._order):
            for col_idx in range(self._order):
                flow = self._flow_matrix[row_idx][col_idx]
                capacity = self._capacity_matrix[row_idx][col_idx]
                cost = self._cost_matrix[row_idx][col_idx]

                if capacity > 0:
                    # Запоминаем стоимости для всех потенциальных ребер в остаточной сети.
                    # Даже если сейчас ребро не существует (capacity=0), мы должны знать его цену.
                    cost_residual_matrix[row_idx][col_idx] = cost
                    cost_residual_matrix[col_idx][row_idx] = -cost

                reserve = capacity - flow
                if reserve > 0:
                    residual_matrix[row_idx][col_idx] = reserve

                if flow > 0:
                    residual_matrix[col_idx][row_idx] = flow

        return residual_matrix, cost_residual_matrix

    def _get_cost_by_flow(self) -> int:
        """Возвращает суммарную стоимость транспортировки на основе матрицы локальных потоков
        и матрицы стоимостей"""
        total_cost = 0
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if self._flow_matrix[row_idx][col_idx] > 0:
                    total_cost += self._flow_matrix[row_idx][col_idx] * self._cost_matrix[row_idx][col_idx]
        return total_cost


if __name__ == "__main__":
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    cost_matrix = [
        # s a  b  c  d  t
        [0, 3, 2, 4, 0, 0],  # s
        [0, 0, 0, 4, 5, 0],  # a
        [0, 2, 0, 2, 0, 0],  # b
        [0, 0, 0, 0, 2, 0],  # c
        [0, 0, 0, 0, 0, 1],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока минимальной стоимости:")
    calculator = MinCostFlowCalculator(capacity_matrix, cost_matrix)
    print("Величина максимального потока:", calculator._max_flow)
    print("Стоимость потока:", calculator._min_cost)
    print("Матрица локальных потоков")
    for row in calculator._flow_matrix:
        print(row)
