from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching


def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: паросочетание, представляющее оптимальное назначение.
    :rtype: BipartiteGraphMatching
    """
    matrix_size = len(matrix)
    matching = BipartiteGraphMatching(matrix_size)
    reduced_matrix = get_reduced_matrix(matrix)
       
    while not matching.is_perfect:
        bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
        matching_increased, reachable_left, reachable_right = _try_expand_matching(bipartite_graph, matching)
        
        if not matching_increased:
            reduced_matrix = _diagonal_reduction(reduced_matrix, reachable_left, reachable_right)

    return matching


def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    adjacency_lists = {}
    for row_idx in range(len(reduced_matrix)):
        adjacency_lists[row_idx] = [col_idx for col_idx, value in enumerate(reduced_matrix[row_idx]) if value == 0]
    return BipartiteGraph(adjacency_lists)

def _try_expand_matching(graph: BipartiteGraph, matching: BipartiteGraphMatching) ->tuple[bool, set[int], set[int]]:
    """
    Пытается увеличить паросочетание методом волны.

    :param graph: двудольный граф, построенный по нулевым элементам редуцированной матрицы.
    :type graph: BipartiteGraph
    :param matching: текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :return: кортеж (паросочетание увеличено?, покрытые деревом левые вершины, покрытые деревом правые вершины).
    :rtype:  tuple[bool, set[int], set[int]]
    """
    for left_vertex in range(graph.order):
        if not matching.is_left_covered(left_vertex):
            result = _find_extension_path(graph, matching, left_vertex)
            if result['path'] is not None:
                _increase_along_path(matching, result['path'])
                return True, set(), set()
            else:
                return False, result['reachable_left'], result['reachable_right']
    
    return True, set(), set()

def _find_extension_path(graph: BipartiteGraph, matching: BipartiteGraphMatching, start_vertex: int) -> list[int] | None:
    """
    Находит увеличивающий путь в графе методом волны.
    Строит чередующееся дерево от свободной левой вершины.

    :param graph: двудольный граф.
    :type graph: BipartiteGraph
    :param matching: текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :param start_vertex: индекс свободной левой вершины (корень дерева).
    :type start_vertex: int
    :return: словарь с ключами 'path' (список вершин или None),
             'reachable_left' (множество покрытых деревом левых вершин),
             'reachable_right' (множество покрытых деревом правых вершин).
    :rtype: dict
    """
    parent = [-1] * (2 * graph.order)
    visited_left = [False] * graph.order
    visited_right = [False] * graph.order
    reachable_left = set()
    reachable_right = set()
    queue = deque([start_vertex])
    visited_left[start_vertex] = True
    reachable_left.add(start_vertex)

    while queue:
        current_left = queue.popleft()
        for current_right in graph.right_neighbors(current_left):
            if visited_right[current_right]:
                continue
                
            visited_right[current_right] = True
            reachable_right.add(current_right)
            parent[graph.order + current_right] = current_left
            if not matching.is_right_covered(current_right):
                path = _restore_path(parent, graph.order, current_right)
                return {
                    'path': path,
                    'reachable_left': reachable_left,
                    'reachable_right': reachable_right
                }
            
            paired_left = matching.get_left_match(current_right)
            if not visited_left[paired_left]:
                visited_left[paired_left] = True
                reachable_left.add(paired_left)
                parent[paired_left] = graph.order + current_right
                queue.append(paired_left)
    
    return {
        'path': None,
        'reachable_left': reachable_left,
        'reachable_right': reachable_right
    }

def _restore_path(parent: list[int], graph_size: int, end_right_vertex: int) -> list[int]:
    """
    Восстанавливает увеличивающий путь от корня до конечной вершины.

    :param parent: массив родителей для восстановления пути.
    :type parent: list[int]
    :param graph_size: размер графа.
    :type graph_size: int
    :param end_right_vertex: индекс конечной свободной правой вершины.
    :type end_right_vertex: int
    :return: список вершин пути, чередующихся между левой и правой долями.
    :rtype: list[int]
    """
    path = []
    current_vertex = graph_size + end_right_vertex
    
    while current_vertex != -1:
        path.append(current_vertex)
        current_vertex = parent[current_vertex]
    
    path.reverse()
    return path

def _increase_along_path(matching: BipartiteGraphMatching, path: list[int]) -> None:
    """
    Увеличивает паросочетание вдоль найденного увеличивающего пути.
    Путь чередуется левая -> правая -> левая -> правая -> ....
    Рёбра на нечётных позициях (left -> right) добавляются в паросочетание,
    рёбра на чётных позициях (right -> left) удаляются из паросочетания.

    :param matching: паросочетание для увеличения.
    :type matching: BipartiteGraphMatching
    :param path: увеличивающий путь в виде чередующихся индексов (левая, правая, левая, ...).
    :type path: list[int]
    """
    edges_to_remove = []
    for position in range(1, len(path) - 1, 2):
        right_index = path[position] - matching.order
        left_index = path[position + 1]
        if matching.is_left_covered(left_index):
            old_right = matching.get_right_match(left_index)
            edges_to_remove.append((left_index, old_right))
    
    for left_index, right_index in edges_to_remove:
        matching.remove_edge(left_index, right_index)
    
    for position in range(0, len(path) - 1, 2):
        left_index = path[position]
        right_index = path[position + 1] - matching.order
        matching.add_edge(left_index, right_index)

def _diagonal_reduction(matrix: list[list[int | float]], reachable_left: set[int], reachable_right: set[int]) -> list[list[int | float]]:
    """
    Выполняет диагональную редукцию матрицы для создания дополнительных нулей. 
    Использует информацию о покрытых деревом вершинах, полученную при построении 
    чередующегося дерева методом волны.

    :param matrix: редуцированная матрица.
    :type matrix: list[list[int|float]]
    :param reachable_left: множество покрытых деревом левых вершин (множество X).
    :type reachable_left: set[int]
    :param reachable_right: множество покрытых деревом правых вершин (множество Y).
    :type reachable_right: set[int]
    :return: новая редуцированная матрица с дополнительными нулями.
    :rtype: list[list[int|float]]
    """
    matrix_size = len(matrix)
    
    min_value = float('inf')
    for row in range(matrix_size):
        if row in reachable_left:
            for col in range(matrix_size):
                if col not in reachable_right:
                    min_value = min(min_value, matrix[row][col])
    new_matrix = [row[:] for row in matrix]
    
    for row in range(matrix_size):
        if row in reachable_left:
            for col in range(matrix_size):
                new_matrix[row][col] -= min_value
    
    for row in range(matrix_size):
        for col in range(matrix_size):
            if col in reachable_right:
                new_matrix[row][col] += min_value
    
    return new_matrix

def get_reduced_matrix(matrix: list[list[int | float]]) -> list[list[int | float]]:
    """
    Выполняет редукцию матрицы, уменьшая значения в строках и столбцах.

    :param matrix: Исходная квадратная матрица весов.
    :type matrix: list[list[int|float]]
    :return: Редуцированная матрица, где минимальные значения в строках и столбцах равны 0.
    :rtype: list[list[int|float]]
    """
    reduced_matrix = [[val - min(row) for val in row] for row in matrix]

    for col_idx in range(len(reduced_matrix[0])):
        min_col_value = reduced_matrix[0][col_idx]
        for row_idx in range(1, len(reduced_matrix)):
            if reduced_matrix[row_idx][col_idx] < min_col_value:
                min_col_value = reduced_matrix[row_idx][col_idx]
        for row_idx in range(len(reduced_matrix)):
            reduced_matrix[row_idx][col_idx] -= min_col_value

    return reduced_matrix

if __name__ == "__main__":
    matrix = [
        [6, 7, 8, 14, 7],
        [8, 14, 6, 9, 7],
        [14, 14, 13, 9, 11],
        [5, 12, 10, 9, 14],
        [6, 10, 8, 10, 15],
    ]
    print("Исходная матрица")
    for row in matrix:
        print(row)
    print()

    reduced_matrix = get_reduced_matrix(matrix)
    print("Редуцированная матрица")
    for row in reduced_matrix:
        print(row)
    print()

    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    print("Двудольный граф")
    print(bipartite_graph)
    print()

    matching = hungarian(matrix)
    print("Совершенное паросочетание найденное венгерским алгоритмом")
    print(matching.get_matching())
