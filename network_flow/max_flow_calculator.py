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
                    self._residual_matrix[row_idx][col_idx] = self._capacity_matrix[row_idx][col_idx]

        self._max_flow = None
        self._flow_matrix = None
        # Процедура _calculate_max_flow должна в ходе выполнения заполнить атрибуты _flow_matrix и _max_flow
        self._calculate_max_flow()

    @property
    def max_flow(self) -> int:
        """Возвращает максимальное значение потока
        
        :return: Величина максимального потока от источника к стоку
        :rtype: int
        """
        return self._max_flow

    @property
    def flow_matrix(self) -> tuple[tuple[int]]:
        """Возвращает матрицу локальных потоков
        
        :return: Кортеж кортежей, где flow_matrix[i][j] показывает фактический поток от вершины i к вершине j
        :rtype: Tuple[Tuple[int, ...], ...]
        """
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
        sources = []    
        sinks = []
        transits = []

        vertex_count = len(matrix)

        for vertex_index in range(vertex_count):
            has_outgoing_edges = any(
                matrix[vertex_index][target_index] > 0 
                for target_index in range(vertex_count)
            )

            has_incoming_edges = any(
                matrix[source_index][vertex_index] > 0 
                for source_index in range(vertex_count)
            )

            if has_outgoing_edges and not has_incoming_edges:
                sources.append(vertex_index)
            elif has_incoming_edges and not has_outgoing_edges:
                sinks.append(vertex_index)
            elif has_incoming_edges and has_outgoing_edges:
                transits.append(vertex_index)
        
        return NetworkVerticesData(sources, sinks, transits)

    def _calculate_max_flow(self) -> None:
        """Вычисляет максимальный поток в сети с использованием алгоритма Форда-Фалкерсона"""
        total_flow_value = 0
        while True:
            visited_vertices = [False] * self._order

            augmenting_path = self._find_augmenting_path(self._source_idx, self._sink_idx, visited_vertices, [])

            if augmenting_path is None:
                break

            flow_increment = self._increase_flow(augmenting_path)
            total_flow_value += flow_increment

        self._max_flow = total_flow_value
        self._set_flow_matrix_by_residual_matrix()

    def _set_flow_matrix_by_residual_matrix(self) -> None:
        """Обновляет матрицу локальных потоков на основе остаточной сети"""
        self._flow_matrix = [[0]*self._order for _ in range(self._order)]

        for row_index in range(self._order):
            for col_index in range(self._order):
                original_capacity = self._capacity_matrix[row_index][col_index]
                residual_capacity = self._residual_matrix[row_index][col_index]
                
                if original_capacity > 0:
                    flow_value = original_capacity - residual_capacity
                    self._flow_matrix[row_index][col_index] = flow_value

    def _find_augmenting_path(self, current_vertex, target_vertex, visited_vertices, current_path):
        """Возвращает найденный увеличивающий путь в сети"""
        current_path.append(current_vertex)
        visited_vertices[current_vertex] = True

        if current_vertex == target_vertex:
            return current_path.copy()
        
        for neighbor_vertex in range(self._order):
            has_residual_capacity = self._residual_matrix[current_vertex][neighbor_vertex] > 0
            is_not_visited = neighbor_vertex not in visited_vertices
            is_not_visited = not visited_vertices[neighbor_vertex]

            if has_residual_capacity and is_not_visited:
                found_path = self._find_augmenting_path(neighbor_vertex, target_vertex, visited_vertices, current_path)

                if found_path is not None:
                    return found_path
                
        current_path.pop()
        return None
        

    def _increase_flow(self, augmenting_path) -> int:
        """Корректирует остаточную сеть для увеличения потока в сети с использованием
        найденного увеличивающего пути"""
        bottleneck_capacity = float("inf")
        for vertex_index in range(len(augmenting_path) - 1):
            edge_residual_capacity = self._residual_matrix[augmenting_path[vertex_index]][augmenting_path[vertex_index + 1]]
            bottleneck_capacity = min(bottleneck_capacity, edge_residual_capacity)
        
        for vertex_index in range(len(augmenting_path) - 1):
            self._residual_matrix[augmenting_path[vertex_index]][augmenting_path[vertex_index + 1]] -= bottleneck_capacity
            self._residual_matrix[augmenting_path[vertex_index + 1]][augmenting_path[vertex_index]] += bottleneck_capacity
            
        return bottleneck_capacity


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
