from collections import deque
from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching

def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Матрица смежности, где ``True`` означает включение ребра в паросочетание.
    :rtype: list[list[bool]]
    """
    order = len(matrix)
   
    reduced_matrix = get_reduced_matrix(matrix)
    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    
    matching = BipartiteGraphMatching(order)

    while not matching.is_perfect:
        start_node = -1
        for i in range(order):
            if not matching.is_left_covered(i):
                start_node = i
                break
        
        if start_node == -1:
            break

        path_found, result = _find_chain(bipartite_graph, matching, start_node)

        if path_found:
            _apply_chain(matching, result)
        else:
            visited_left, visited_right = result
            bipartite_graph = _update_matrix_and_graph(reduced_matrix, visited_left, visited_right)
            
    return matching


def _find_chain(graph: BipartiteGraph, matching: BipartiteGraphMatching, start_node: int):
    """
    Ищет увеличивающую цепь с использованием BFS (метод волны).
    :return: (True, (end_right_node, parent_map)) если найден путь,
             (False, (visited_left, visited_right)) если путь не найден.
    """
    queue = deque([start_node])
    
    parent_of_right = {} 
    
    visited_left = {start_node}
    visited_right = set()
    
    while queue:
        left_top = queue.popleft()
        
        neighbors = graph.right_neighbors(left_top)
        for right_top in neighbors:
            if right_top in visited_right:
                continue
            
            visited_right.add(right_top)
            parent_of_right[right_top] = left_top
            
            if not matching.is_right_covered(right_top):
                return True, (right_top, parent_of_right)
            
            left_top_after_right = matching.get_left_match(right_top)
            if left_top_after_right not in visited_left:
                visited_left.add(left_top_after_right)
                queue.append(left_top_after_right)
    
    return False, (visited_left, visited_right)


def _apply_chain(matching: BipartiteGraphMatching, result: tuple):
    """
    Применяет увеличивающую цепь к текущему паросочетанию.
    """
    curr_r, parent_map = result
    
    while True:
        curr_l = parent_map[curr_r]
        
        prev_match_r = -1
        if matching.is_left_covered(curr_l):
            prev_match_r = matching.get_right_match(curr_l)
            matching.remove_edge(curr_l, prev_match_r)
        
        matching.add_edge(curr_l, curr_r)
        
        if prev_match_r == -1:
            break
            
        curr_r = prev_match_r


def _update_matrix_and_graph(reduced_matrix, visited_left, visited_right):
    """
    Выполняет диагональную редукцию и возвращает обновленный граф.
    """
    rows_count = len(reduced_matrix)
    cols_count = len(reduced_matrix[0])
    
    min_elem = float('inf')
    for row in visited_left:
        for column in range(cols_count):
            if column not in visited_right:
                if reduced_matrix[row][column] < min_elem:
                    min_elem = reduced_matrix[row][column]
    
    if min_elem == float('inf'):
         raise ValueError("")

    for row in range(rows_count):
        if row in visited_left:
            for column in range(cols_count):
                reduced_matrix[row][column] -= min_elem
    
    for column in range(cols_count):
        if column in visited_right:
            for row in range(rows_count):
                reduced_matrix[row][column] += min_elem

    return _get_bipartite_graph_by_zeros(reduced_matrix)

def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    adjacency_lists = {}
    for row_idx in range(len(reduced_matrix)):
        adjacency_lists[row_idx] = [col_idx for col_idx, value in enumerate(reduced_matrix[row_idx]) if value == 0]
    return BipartiteGraph(adjacency_lists)


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
