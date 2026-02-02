from collections import deque

from matching.bipartite_graph import BipartiteGraph
from matching.bipartite_graph_matching import BipartiteGraphMatching


EPS = 1e-10
FLOAT_MAX = 1e100 


def hungarian(matrix: list[list[int | float]]) -> BipartiteGraphMatching:
    """
    Реализация венгерского алгоритма для решения задачи о назначениях.

    :param matrix: Квадратная матрица весов, где ``matrix[i][j]`` представляет вес назначения ``i -> j``.
    :type matrix: list[list[int|float]]
    :return: Матрица смежности, где ``True`` означает включение ребра в паросочетание.
    :rtype: list[list[bool]]
    """
    order = len(matrix)
    matching = BipartiteGraphMatching(order)
    reduced_matrix = get_reduced_matrix(matrix)
    bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    
    while not matching.is_perfect:
        augmenting_path = find_augmenting_path(bipartite_graph, matching)
        
        if augmenting_path:
            update_matching_with_augmenting_path(matching, augmenting_path)
        else:
            S, T = get_sets_from_bfs(bipartite_graph, matching)
            delta = calculate_min(reduced_matrix, S, T)
            update_reduced_matrix(reduced_matrix, S, T, delta)
            bipartite_graph = _get_bipartite_graph_by_zeros(reduced_matrix)
    
    return matching


def find_augmenting_path(
    bipartite_graph: BipartiteGraph, 
    matching: BipartiteGraphMatching
) -> list[int]:
    """
    Находит цепь в двудольном графе на основе текущего паросочетания.

    :param bipartite_graph: Двудольный граф
    :type bipartite_graph: BipartiteGraph
    :param matching: Текущее паросочетание в графе
    :type matching: BipartiteGraphMatching
    :return: Список вершин, образующих цепь, или пустой список, если цепь не найдена
    :rtype: list[int]
    """
    order = matching.order
    parent_row = {}
    parent_col = {}
    visited_row = [False] * order
    visited_col = [False] * order
    queue = deque()
    
    free_lefts = get_free_left_vertices(matching)
    for i in free_lefts:
        visited_row[i] = True
        queue.append(i)
    
    found = False
    free_col = -1
    
    while queue and not found:
        row = queue.popleft()
        
        for col in bipartite_graph.right_neighbors(row):
            if not visited_col[col]:
                visited_col[col] = True
                parent_col[col] = row
                
                if matching.get_left_match(col) == -1:
                    found = True
                    free_col = col
                    break
                else:
                    matched_row = matching.get_left_match(col)
                    if not visited_row[matched_row]:
                        visited_row[matched_row] = True
                        parent_row[matched_row] = col
                        queue.append(matched_row)
    
    if not found:
        return []
    
    return reconstruct_augmenting_path(free_col, parent_row, parent_col)


def get_free_left_vertices(matching: BipartiteGraphMatching) -> list[int]:
    """
    Возвращает список свободных вершин слева

    :param matching: Текущее паросочетание в графе
    :type matching: BipartiteGraphMatching
    :return: Список индексов свободных вершин слева
    :rtype: list[int]
    """
    return [i for i in range(matching.order) if matching.get_right_match(i) == -1]


def reconstruct_augmenting_path(
    free_col: int, 
    parent_row: dict, 
    parent_col: dict
) -> list[int]:
    """
    Восстанавливает цепь по родительским ссылкам

    :param free_col: Индекс свободной вершины справа, с которой начинается цепь
    :type free_col: int
    :param parent_row: Словарь родительских ссылок для вершин слева
    :type parent_row: dict
    :param parent_col: Словарь родительских ссылок для вершин справа
    :type parent_col: dict
    :return: Список вершин, образующих цепь
    :rtype: list[int]
    """
    path = []
    current = free_col
    
    while current is not None:
        path.append(current)
        row = parent_col.get(current, None)
        if row is None:
            break
        path.append(row)
        current = parent_row.get(row, None)
    
    path.reverse()
    return path


def update_matching_with_augmenting_path(
    matching: BipartiteGraphMatching, 
    augmenting_path: list[int]
) -> None:
    """
    Обновляет паросочетание с использованием найденной цепи

    :param matching: Текущее паросочетание
    :type matching: BipartiteGraphMatching
    :param augmenting_path: Список вершин, образующих цепь
    :type augmenting_path: list[int]
    :return: None
    :rtype: None
    """
    lefts = [augmenting_path[k] for k in range(0, len(augmenting_path), 2)]
    for left in lefts:
        if matching.is_left_covered(left):
            right = matching.get_right_match(left)
            matching.remove_edge(left, right)
    

    for k in range(0, len(augmenting_path) - 1, 2):
        left = augmenting_path[k]
        right = augmenting_path[k + 1]
        matching.add_edge(left, right)


def get_sets_from_bfs(
    bipartite_graph: BipartiteGraph, 
    matching: BipartiteGraphMatching
) -> tuple:
    """
    Выполняет BFS для получения множеств вершины слева и вершины справа для обновления матрицы

    :param bipartite_graph: Двудольный граф
    :type bipartite_graph: BipartiteGraph
    :param matching: Текущее паросочетание в графе
    :type matching: BipartiteGraphMatching
    :return: Кортеж из двух списков вершин слева и вершин справа
    :rtype: tuple[list[int], list[int]]
    """
    order = matching.order
    visited_row = [False] * order
    visited_col = [False] * order
    queue = deque()
    
    free_lefts = get_free_left_vertices(matching)
    for i in free_lefts:
        visited_row[i] = True
        queue.append(i)
    
    while queue:
        row = queue.popleft()
        
        for col in bipartite_graph.right_neighbors(row):
            if not visited_col[col]:
                visited_col[col] = True
                
                matched_row = matching.get_left_match(col)
                if matched_row != -1 and not visited_row[matched_row]:
                    visited_row[matched_row] = True
                    queue.append(matched_row)
    
    S = [i for i in range(order) if visited_row[i]]
    T = [j for j in range(order) if visited_col[j]]
    
    return S, T


def calculate_min(
    reduced_matrix: list[list[float]],
    S: list[int],
    T: list[int]
) -> float:
    """
    Вычисляет минимальное значение в редуцированной матрице

    :param reduced_matrix: Редуцированная матрица
    :type reduced_matrix: list[list[float]]
    :param S: Множество вершин слева
    :type S: list[int]
    :param T: Множество вершин справа
    :type T: list[int]
    :return: Минимальное значение для обновления матрицы
    :rtype: float
    """
    order = len(reduced_matrix)
    delta = FLOAT_MAX
    
    T_set = set(T) 
    
    for i in S:
        for j in range(order):
            if j not in T_set:
                if reduced_matrix[i][j] < delta:
                    delta = reduced_matrix[i][j]
    
    return delta


def update_reduced_matrix(
    reduced_matrix: list[list[float]],
    S: list[int],
    T: list[int],
    delta: float
) -> None:
    """
    Обновляет редуцированную матрицу по алгоритму

    :param reduced_matrix: Редуцированная матрица
    :type reduced_matrix: list[list[float]]
    :param S: Множество вершин слева
    :type S: list[int]
    :param T: Множество вершин справа
    :type T: list[int]
    :param delta: Значение для обновления матрицы
    :type delta: float
    :return: None
    :rtype: None
    """
    order = len(reduced_matrix)
    T_set = set(T)  
    
    for i in S:
        for j in range(order):
            reduced_matrix[i][j] -= delta
    
    for j in T:
        for i in range(order):
            reduced_matrix[i][j] += delta


def _get_bipartite_graph_by_zeros(reduced_matrix: list[list[int | float]]) -> BipartiteGraph:
    """
    Строит двудольный граф на основе нулевых элементов в редуцированной матрице

    :param reduced_matrix: Редуцированная матрица
    :type reduced_matrix: list[list[int|float]]
    :return: Двудольный граф, где ребра соответствуют нулевым элементам.
    :rtype: BipartiteGraph
    """
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
