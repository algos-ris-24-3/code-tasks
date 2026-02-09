from collections import namedtuple


INF = float("inf")

ShortestPath = namedtuple("ShortestPath", ["distance", "path"])
"""
    Структура данных для хранения информации о кратчайшем пути между вершинами.

    :param distance: Длина кратчайшего пути от исходной вершины до целевой. 
                     Если путь недостижим, значение `None`.
    :type distance: Optional[int]
    :param path: Список индексов вершин, представляющий маршрут кратчайшего пути. 
                 Если путь отсутствует, возвращается пустой список.
    :type path: list[int]
    """
