from collections import namedtuple
from math import inf

ShortestPathData = namedtuple(
    "ShortestPathData",
    "distance path",
)
"""
    Структура данных для хранения информации о кратчайшем пути между вершинами.

    :param distance: Длина кратчайшего пути от исходной вершины до целевой. 
                     Если путь недостижим, значение `None`.
    :type distance: Optional[int]
    :param path: Список индексов вершин, представляющий маршрут кратчайшего пути. 
                 Если путь отсутствует, возвращается пустой список.
    :type path: list[int]
    """

MATRIX_ERR_MSG = "Таблица расстояний не является квадратной матрицей с целыми неотрицательными значениями"
EMPTY_MATRIX_ERR_MSG = "Таблица расстояний пуста"
SRC_ERR_MSG = "Индекс исходной вершины должен быть неотрицательным целым числом меньшим чем порядок таблицы"
TRG_ERR_MSG = "Индекс целевой вершины должен быть неотрицательным целым числом меньшим чем порядок таблицы"
NEGATIVE_LOOP_ERR_MSG = "В графе имеется цикл отрицательной стоимости"


class NegativeLoopFloydWarshallError(RuntimeError):
    def __init__(self, detected_vertex_idx):
        self.detected_vertex_idx = detected_vertex_idx
        super().__init__(NEGATIVE_LOOP_ERR_MSG)


def get_shortest_path(
    dist_matrix: list[list[int]], source_idx: int, target_idx: int
) -> ShortestPathData:
    """
    Вычисляет кратчайший путь между двумя вершинами графа с использованием алгоритма Флойда-Уоршелла.

    :param dist_matrix: Квадратная матрица расстояний, где `dist_matrix[i][j]` представляет вес ребра (i, j).
                        Если между вершинами нет прямого пути, значение `None`.
    :type dist_matrix: list[list[int]]
    :param source_idx: Индекс начальной вершины.
    :type source_idx: int
    :param target_idx: Индекс целевой вершины.
    :type target_idx: int
    :return: Объект `ShortestPathData`, содержащий:
             - `distance`: минимальное расстояние от `source_idx` до `target_idx` (или `None`, если путь недостижим).
             - `path`: список вершин, представляющий кратчайший путь (пустой, если путь отсутствует).
    :rtype: ShortestPathData
    :raises ValueError: Если входные параметры некорректны.
    :raises NegativeLoopFloydWarshallError: Если в графе обнаружен цикл отрицательной стоимости.
    """
    __validate_params(dist_matrix, source_idx, target_idx)
    if source_idx == target_idx:
        return ShortestPathData(0, [])
    distances = floyd_warshall(dist_matrix)
    if distances[source_idx][target_idx] == inf:
        return ShortestPathData(None, [])
    shortest_path = __restore_path(dist_matrix, distances, source_idx, target_idx)
    return ShortestPathData(distances[source_idx][target_idx], shortest_path)


def floyd_warshall(dist_matrix: list[list[int]]) -> tuple[list[int], list[int]]:
    """
    Реализует алгоритм Флойда-Уоршелла для поиска кратчайших расстояний между всеми парами вершин.

    :param dist_matrix: Квадратная матрица расстояний, где `dist_matrix[i][j]` — вес ребра (i, j).
                        Если вершины не соединены, значение `None`.
    :type dist_matrix: list[list[int]]
    :return: Матрица `dist`, где `dist[i][j]` содержит кратчайшее расстояние от вершины `i` к `j`.
             Если `i == j`, то `dist[i][i] = 0`.
             Если `j` недостижима из `i`, то `dist[i][j] = inf`.
    :rtype: list[list[int]]
    :raises NegativeLoopFloydWarshallError: Если в графе обнаружен цикл отрицательной стоимости.
    """
    order = len(dist_matrix)
    distances = [[dist_matrix[i][j] or inf for j in range(order)] for i in range(order)]
    for k in range(order):
        for vertex_idx in range(order):
            for j in range(order):
                has_path = distances[vertex_idx][k] < inf and distances[k][j] < inf
                is_shorter = (
                    distances[vertex_idx][k] + distances[k][j]
                    < distances[vertex_idx][j]
                )
                if has_path and is_shorter:
                    distances[vertex_idx][j] = (
                        distances[vertex_idx][k] + distances[k][j]
                    )

        for vertex_idx in range(order):
            if distances[vertex_idx][vertex_idx] < 0:
                raise NegativeLoopFloydWarshallError(vertex_idx)
    return distances


def __restore_path(
    dist_matrix: list[list[int]],
    dist: list[list[int]],
    source_idx: int,
    target_idx: int,
) -> list[int]:
    """
    Восстанавливает кратчайший путь от начальной вершины до целевой на основе матрицы расстояний.

    :param dist_matrix: Исходная матрица расстояний, содержащая веса рёбер графа.
    :type dist_matrix: list[list[int]]
    :param dist: Матрица кратчайших расстояний, полученная с помощью `__floyd_warshall`.
    :type dist: list[list[int]]
    :param source_idx: Индекс начальной вершины.
    :type source_idx: int
    :param target_idx: Индекс целевой вершины.
    :type target_idx: int
    :return: Список индексов вершин, представляющий кратчайший путь от `source_idx` до `target_idx`.
             Если путь отсутствует, возвращается пустой список.
    :rtype: list[int]
    """
    path_back = [target_idx]
    cur_vertex_idx = target_idx
    dist_to_src = dist[source_idx][target_idx]
    while cur_vertex_idx != source_idx:
        for i in range(len(dist_matrix)):
            cur_dist = dist_matrix[i][cur_vertex_idx]
            dist_cur_to_source = dist[source_idx][i] if source_idx != i else 0
            if cur_dist and cur_dist + dist_cur_to_source == dist_to_src:
                path_back.append(i)
                cur_vertex_idx = i
                dist_to_src -= cur_dist
                break
    return path_back[::-1]


def __validate_params(dist_matrix: list[list[int]], source_idx: int, target_idx: int):
    """
    Проверяет корректность входных параметров для алгоритма поиска кратчайшего пути.

    Этот метод выполняет валидацию матрицы расстояний и индексов начальной и целевой вершин.
    Если параметры не соответствуют требованиям, выбрасывается исключение ValueError с соответствующим сообщением.

    Параметры:
        dist_matrix (list[list[int]]): Матрица расстояний, где каждый элемент — это либо неотрицательное целое число, либо `None`.
                                       Матрица должна быть квадратной и удовлетворять условиям, указанным в `__validate_matrix`.
        source_idx (int): Индекс исходной вершины. Должен быть целым числом от 0 до размера матрицы (не включительно).
        target_idx (int): Индекс целевой вершины. Должен быть целым числом от 0 до размера матрицы (не включительно).

    Исключения:
        ValueError: Выбрасывается в следующих случаях:
            - Если `dist_matrix` не соответствует требованиям (проверяется в `__validate_matrix`).
            - Если `source_idx` не является целым числом или выходит за границы допустимого диапазона (от 0 до порядка матрицы).
            - Если `target_idx` не является целым числом или выходит за границы допустимого диапазона (от 0 до порядка матрицы).
    """
    __validate_matrix(dist_matrix)

    order = len(dist_matrix)
    if not isinstance(source_idx, int) or source_idx < 0 or source_idx >= order:
        raise ValueError(SRC_ERR_MSG)
    if not isinstance(target_idx, int) or target_idx < 0 or target_idx >= order:
        raise ValueError(TRG_ERR_MSG)


def __validate_matrix(matrix: list[list[int]]) -> None:
    """
    Проверяет корректность матрицы расстояний.

    Этот метод выполняет валидацию матрицы расстояний для алгоритма поиска кратчайшего пути.
    Если матрица не соответствует требованиям, выбрасывается исключение ValueError с соответствующим сообщением.

    Параметры:
        matrix (list[list[int]]): Матрица расстояний, где каждый элемент — это либо неотрицательное целое число, либо `None`.
                                  Матрица должна быть квадратной и не содержать отрицательных значений.

    Исключения:
        ValueError: Выбрасывается в следующих случаях:
            - Если `matrix` не является списком.
            - Если `matrix` пуста.
            - Если строки `matrix` не являются списками.
            - Если `matrix` не является квадратной матрицей (число строк не равно числу столбцов).
            - Если в `matrix` содержатся значения, не являющиеся неотрицательными целыми числами или `None`.
    """
    if not isinstance(matrix, list):
        raise ValueError(MATRIX_ERR_MSG)
    if not matrix:
        raise ValueError(EMPTY_MATRIX_ERR_MSG)
    if not isinstance(matrix[0], list):
        raise ValueError(MATRIX_ERR_MSG)
    if not matrix[0]:
        raise ValueError(EMPTY_MATRIX_ERR_MSG)

    rows_cnt = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != rows_cnt:
            raise ValueError(MATRIX_ERR_MSG)
        for value in row:
            if not isinstance(value, (int, type(None))):
                raise ValueError(MATRIX_ERR_MSG)


def main():
    matrix = [[0, None, None], [1, 0, None], [None, 1, 0]]
    src = 2
    trg = 0

    print("Исходная матрица")
    for row in matrix:
        print(row)

    result = get_shortest_path(matrix, src, trg)
    print(f"\nКратчайшее расстояние между вершинами {src} и {trg} составляет:")
    print(result.distance)
    print("Путь:")
    print(result.path)


if __name__ == "__main__":
    main()
