from typing import Dict, List

from matching.errors.error_message_template_enum import ErrorMessageTemplateEnum
from matching.errors.error_message_enum import ErrorMessageEnum


class BipartiteGraph:
    """
    Представление двудольного графа с долями равной мощности.

    Граф задаётся списками смежности для вершин левой доли.
    Каждая вершина левой доли имеет индекс в диапазоне [0, order),
    каждая вершина правой доли — также в диапазоне [0, order).

    Ограничения:
    - Обе доли должны иметь одинаковую мощность (order).
    - Все ключи adjacency_dict должны быть целыми числами из [0, order).
    - Все значения в списках смежности должны быть целыми числами из [0, order).
    - Не допускаются дубликаты в списках смежности.
    """

    def __init__(self, adjacency_lists: Dict[int, List[int]]):
        """
        Инициализирует двудольный граф на основе словаря смежности левой доли.

        :param adjacency_lists: Списки смежности для вершин левой доли.
        :raises ValueError: Если входные данные нарушают ограничения графа.
        """
        self._validate_adjacency_lists(adjacency_lists)

        self._order = len(adjacency_lists)
        self._adjacency_lists = {key: list(value) for key, value in adjacency_lists.items()}
    
    def __repr__(self) -> str:
        """
        Возвращает строковое представление двудольного графа.

        Формат: BipartiteGraph(order=N, adjacency={...})
        где N — мощность каждой доли, а adjacency — словарь смежности левой доли.
        """
        return f"BipartiteGraph(order={self._order}, adjacency={self._adjacency_lists})"
    
    @property
    def order(self) -> int:
        """
        Мощность каждой доли графа (левой и правой).

        Все вершины в обеих долях имеют индексы в диапазоне [0, order).
        """
        return self._order

    def right_neighbors(self, idx: int) -> List[int]:
        """
        Возвращает список индексов вершин правой доли, смежных с левой вершиной `idx`.

        :param idx: Индекс вершины в левой доле (0 <= idx < order)
        :return: Список индексов смежных вершин правой доли (может быть пустым)
        :raises IndexError: Если `idx` выходит за пределы [0, order)
        """
        if not (0 <= idx < self._order):
            raise IndexError(ErrorMessageTemplateEnum.IDX_ERROR.format(idx))
        return self._adjacency_lists[idx].copy()
    

    def _validate_adjacency_lists(self, adjacency_lists: dict) -> int:
        """
        Валидирует списки смежности для двудольного графа с долями равной мощности.

        Проверяет, что:
        - Аргумент является словарём.
        - Ключи — все целые числа от 0 до order-1 (где order = количество ключей).
        - Все значения — списки (или кортежи), состоящие из целых чисел в диапазоне [0, order).

        :param adjacency_lists: Списки смежности для вершин левой доли.
        :return: Порядок графа (order) — количество вершин в каждой доле.
        :raises ValueError: Если входные данные не соответствуют требованиям.
        """
        if not isinstance(adjacency_lists, dict):
            raise ValueError(ErrorMessageEnum.WRONG_ADJACENCY)

        if not adjacency_lists:
            return

        keys = list(adjacency_lists.keys())
        order = len(keys)

        if set(keys) != set(range(order)):
            raise ValueError(ErrorMessageEnum.WRONG_LEFT_IDX)

        for left_vertex, neighbors in adjacency_lists.items():
            if not isinstance(neighbors, (list, tuple)):
                raise ValueError(ErrorMessageTemplateEnum.WRONG_RIGHT_IDX.format(left_vertex))
            if len(neighbors) != len(set(neighbors)):
                raise ValueError(ErrorMessageTemplateEnum.DUPLICATES.format(left_vertex))
            for right_vertex in neighbors:
                if not isinstance(right_vertex, int):
                    raise ValueError(ErrorMessageTemplateEnum.NOT_INT.format(right_vertex))
                if not (0 <= right_vertex < order):
                    raise IndexError(ErrorMessageTemplateEnum.IDX_ERROR.format(right_vertex))

if __name__ == "__main__":
    print("Создаём двудольный граф с долями мощности 4")
    graph = BipartiteGraph({
        0: [1, 2],
        1: [0, 3],
        2: [1],
        3: [2, 3]
    })
    print(graph)

    print("\nМощность каждой доли:")
    print(graph.order)

    print("\nСоседи левой вершины 0:")
    print(graph.right_neighbors(0))

    print("\nСоседи левой вершины 2:")
    print(graph.right_neighbors(2))

    print("\nПопытка запросить соседей несуществующей вершины вызовет ошибку:")
    try:
        graph.right_neighbors(5)
    except IndexError as ex:
        print(ex)

    print("\nПопытка создать граф с пропущенным ключом вызовет ошибку:")
    try:
        BipartiteGraph({
            0: [1],
            2: [0]
        })
    except ValueError as ex:
        print(ex)

    print("\nПопытка создать граф с соседом вне диапазона вызовет ошибку:")
    try:
        BipartiteGraph({
            0: [1],
            1: [5]
        })
    except ValueError as ex:
        print(ex)