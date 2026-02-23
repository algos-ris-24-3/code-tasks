from collections import deque
from math import inf
from network_flow.data_types import NetworkVerticesData
from network_flow.network_validator import NetworkValidator

CAPACITY_MATRIX_NAME = "Таблица пропускных способностей"


class MaxFlowCalculator:
    """Класс для решения задачи поиска максимального потока в сети"""

    def __init__(self, capacity_matrix: list[list[int]]):
        """
        Конструктор класса.

        :param capacity_matrix: Квадратная матрица пропускных способностей графа.
        :type capacity_matrix: list[list[int]]
        """

        NetworkValidator.validate_matrix(capacity_matrix, CAPACITY_MATRIX_NAME)
        vertices = MaxFlowCalculator.split_vertices_by_types(capacity_matrix)
        NetworkValidator.validate_vertices(vertices, CAPACITY_MATRIX_NAME)

        self._capacity_matrix = capacity_matrix
        self._order = len(capacity_matrix)
        self._source_idx = vertices.sources[0]
        self._sink_idx = vertices.sinks[0]

        self._residual_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if capacity_matrix[row_idx][col_idx]:
                    self._residual_matrix[col_idx][row_idx] = self._capacity_matrix[
                        row_idx
                    ][col_idx]

        self._max_flow = None
        self._flow_matrix = None
        self._calculate_max_flow()

    @property
    def max_flow(self) -> int:
        """Возвращает максимальное значение потока"""
        return self._max_flow

    @property
    def flow_matrix(self) -> tuple[tuple[int]]:
        """Возвращает матрицу локальных потоков"""
        return tuple([tuple(row) for row in self._flow_matrix])

    @staticmethod
    def split_vertices_by_types(matrix) -> NetworkVerticesData:
        """
        Разделяет вершины сети на три категории: источники, стоки и транзитные вершины.

        :param matrix: Квадратная матрица пропускных способностей графа.
        :type matrix: list[list[int]]
        :return: Данные о вершинах сети, содержащие источники, стоки и транзиты.
        :rtype: NetworkVerticesData
        """
        order = len(matrix)

        sources = []
        for col_idx in range(order):
            if sum([matrix[row_idx][col_idx] for row_idx in range(order)]) == 0:
                sources.append(col_idx)

        sinks = []
        for row_idx in range(order):
            if sum(matrix[row_idx]) == 0:
                sinks.append(row_idx)

        transits = [idx for idx in range(len(matrix)) if idx not in sources + sinks]

        return NetworkVerticesData(sources, sinks, transits)

    def _calculate_max_flow(self) -> None:
        """Вычисляет максимальный поток в сети с использованием алгоритма Форда-Фалкерсона"""
        augmenting_path = self._find_augmenting_path()

        while augmenting_path:
            self._increase_flow(augmenting_path)
            augmenting_path = self._find_augmenting_path()

        self._set_flow_matrix_by_residual_matrix()
        self._max_flow = sum(self._flow_matrix[self._source_idx])

    def _set_flow_matrix_by_residual_matrix(self):
        """Обновляет матрицу локальных потоков на основе остаточной сети"""
        flow_matrix = [[0] * self._order for _ in range(self._order)]
        for row_idx in range(self._order):
            for col_idx in range(self._order):
                if self._capacity_matrix[row_idx][col_idx]:
                    flow_matrix[row_idx][col_idx] = self._residual_matrix[row_idx][
                        col_idx
                    ]
        self._flow_matrix = flow_matrix

    def _find_augmenting_path(self):
        """Возвращает найденный увеличивающий путь в сети"""
        used = [False] * self._order
        used[self._sink_idx] = True
        first_path = [self._sink_idx]
        queue = deque([first_path])

        while queue:
            path = queue.popleft()
            last_vertex = path[-1]

            for next_vertex in [
                next_vertex
                for next_vertex in range(self._order)
                if self._residual_matrix[last_vertex][next_vertex]
                and not used[next_vertex]
            ]:
                used[next_vertex] = True
                if next_vertex == self._source_idx:
                    return path + [next_vertex]
                queue.append(path + [next_vertex])
        return []

    def _increase_flow(self, augmenting_path):
        """Корректирует остаточную сеть для увеличения потока в сети с использованием
        найденного увеличивающего пути"""
        min_weight = inf
        for idx in range(1, len(augmenting_path)):
            src = augmenting_path[idx - 1]
            trg = augmenting_path[idx]
            min_weight = min(min_weight, self._residual_matrix[src][trg])

        for idx in range(1, len(augmenting_path)):
            src = augmenting_path[idx - 1]
            trg = augmenting_path[idx]
            self._residual_matrix[src][trg] -= min_weight
            self._residual_matrix[trg][src] += min_weight

if __name__ == "__main__":
    vertex_names = ["s", "a", "b", "c", "d", "t"]
    capacity_matrix = [
        # s a  b  c  d  t
        [0, 7, 7, 7, 0, 0],  # s
        [0, 0, 0, 6, 9, 0],  # a
        [0, 6, 0, 5, 0, 0],  # b
        [0, 0, 0, 0, 11, 0],  # c
        [0, 0, 0, 0, 0, 13],  # d
        [0, 0, 0, 0, 0, 0],  # t
    ]
    print("Матрица пропускной способности")
    for row in capacity_matrix:
        print(row)

    print("\nПример решения задачи поиска максимального потока в сети:")
    max_flow_data = MaxFlowCalculator(capacity_matrix)
    print("Величина максимального потока:", max_flow_data.max_flow)
    print("Матрица локальных потоков")
    for row in max_flow_data.flow_matrix:
        print(row)
