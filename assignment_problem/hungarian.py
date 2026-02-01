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
        matching_increased = _try_expand_matching(bipartite_graph, matching)
        
        if not matching_increased:
            reduced_matrix = _diagonal_reduction(reduced_matrix, bipartite_graph, matching)

    return matching


def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    adjacency_lists = {}
    for row_idx in range(len(reduced_matrix)):
        adjacency_lists[row_idx] = [col_idx for col_idx, value in enumerate(reduced_matrix[row_idx]) if value == 0]
    return BipartiteGraph(adjacency_lists)

def _try_expand_matching(graph: BipartiteGraph, matching: BipartiteGraphMatching) -> bool:
    """
    Пытается увеличить паросочетание методом волны (BFS с чередующимся деревом).

    :param graph: двудольный граф, построенный по нулевым элементам редуцированной матрицы.
    :type graph: BipartiteGraph
    :param matching: текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :return: True, если паросочетание было увеличено, иначе False.
    :rtype: bool
    """
    for left_vertex in range(graph.order):
        if not matching.is_left_covered(left_vertex):
            extension_path = _find_extension_path(graph, matching, left_vertex)
            if extension_path:
                _increase_along_path(matching, extension_path)
                return True
    return False

def _find_extension_path(graph: BipartiteGraph, matching: BipartiteGraphMatching, start_vertex: int) -> list[int] | None:
    """
    Находит увеличивающий путь в графе методом волны.
    Строит чередующееся дерево от свободной левой вершины.

    :param graph: Двудольный граф.
    :type graph: BipartiteGraph
    :param matching: Текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :param start_vertex: Индекс свободной левой вершины (корень дерева).
    :type start_vertex: int
    :return: Список вершин увеличивающего пути или None, если путь не найден.
    :rtype: list[int] | None
    """
    graph_size = graph.order
    
    parent = [-1] * (2 * graph_size)
    visited_left = [False] * graph_size
    visited_right = [False] * graph_size
    
    queue = deque([start_vertex])
    visited_left[start_vertex] = True
    
    while queue:
        current_left = queue.popleft()
        for current_right in graph.right_neighbors(current_left):
            if visited_right[current_right]:
                continue
                
            visited_right[current_right] = True
            parent[graph_size + current_right] = current_left
            if not matching.is_right_covered(current_right):
                return _restore_path(parent, graph_size, current_right)
            
            paired_left = matching.get_left_match(current_right)
            if not visited_left[paired_left]:
                visited_left[paired_left] = True
                parent[paired_left] = graph_size + current_right
                queue.append(paired_left)
    
    return None

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
    graph_size = matching.order
    edges_to_remove = []
    for position in range(1, len(path) - 1, 2):
        right_index = path[position] - graph_size
        left_index = path[position + 1]
        if matching.is_left_covered(left_index):
            old_right = matching.get_right_match(left_index)
            edges_to_remove.append((left_index, old_right))
    
    for left_index, right_index in edges_to_remove:
        matching.remove_edge(left_index, right_index)
    
    for position in range(0, len(path) - 1, 2):
        left_index = path[position]
        right_index = path[position + 1] - graph_size
        matching.add_edge(left_index, right_index)

def _diagonal_reduction(matrix: list[list[int | float]], graph: BipartiteGraph, matching: BipartiteGraphMatching) -> list[list[int | float]]:
    """
    Выполняет диагональную редукцию матрицы для создания дополнительных нулей. 
    Находит минимальный элемент среди непокрытых вершин и вычитает его 
    из строк с непокрытыми левыми вершинами, добавляет к столбцам с покрытыми 
    правыми вершинами.

    :param matrix: редуцированная матрица.
    :type matrix: list[list[int|float]]
    :param graph: двудольный граф.
    :type graph: BipartiteGraph
    :param matching: текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :return: новая редуцированная матрица с дополнительными нулями.
    :rtype: list[list[int|float]]
    """
    matrix_size = len(matrix)
    reachable_left, reachable_right = _find_reachable_vertices(graph, matching)
    
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

def _find_reachable_vertices(graph: BipartiteGraph, matching: BipartiteGraphMatching) -> tuple[set[int], set[int]]:
    """
    Находит все вершины, достижимые из свободных левых вершин по чередующимся путям.

    :param graph: двудольный граф.
    :type graph: BipartiteGraph
    :param matching: текущее паросочетание.
    :type matching: BipartiteGraphMatching
    :return: кортеж из двух множеств (достижимые левые вершины, достижимые правые вершины).
    :rtype: tuple[set[int], set[int]]
    """
    graph_size = graph.order
    reachable_left = set()
    reachable_right = set()
    visited_left = [False] * graph_size
    visited_right = [False] * graph_size
    queue = deque()

    for left_vertex in range(graph_size):
        if not matching.is_left_covered(left_vertex):
            queue.append(left_vertex)
            visited_left[left_vertex] = True
            reachable_left.add(left_vertex)
    
    while queue:
        current_left = queue.popleft()
        
        for right_vertex in graph.right_neighbors(current_left):
            if not visited_right[right_vertex]:
                visited_right[right_vertex] = True
                reachable_right.add(right_vertex)
                
                if matching.is_right_covered(right_vertex):
                    paired_left = matching.get_left_match(right_vertex)
                    if not visited_left[paired_left]:
                        visited_left[paired_left] = True
                        reachable_left.add(paired_left)
                        queue.append(paired_left)
    
    return reachable_left, reachable_right

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
