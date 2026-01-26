from matching.errors.error_message_enum import ErrorMessageEnum
from matching.errors.error_message_template_enum import ErrorMessageTemplateEnum


class BipartiteGraphMatching:
    """
    Класс для хранения и управления паросочетанием в двудольном графе,
    в котором левая и правая доли имеют одинаковую мощность.

    Паросочетание представлено двумя взаимосогласованными массивами:
    - `_match_left[i]` содержит индекс вершины из правой доли, сопоставленной 
    вершине `i` из левой доли, либо -1, если вершина `i` не покрыта;
    - `_match_right[j]` содержит индекс вершины из левой доли, сопоставленной 
    вершине `j` из правой доли, либо -1, если вершина `j` не покрыта.
    """

    def __init__(self, order: int):
        """
        Инициализирует пустое паросочетание для двудольного графа с долями мощности `order`.
        
        :param order: Мощность каждой доли (левой и правой)
        """
        if not isinstance(order, int) or order < 0:
            raise ValueError(ErrorMessageEnum.WRONG_ORDER)
            
        self._order = order
        self._match_left = [-1] * order
        self._match_right = [-1] * order
        self._cardinality = 0

    @property
    def order(self) -> int:
        """Мощность каждой доли."""
        return self._order
    
    @property
    def is_perfect(self) -> bool:
        """
        Проверяет, является ли текущее паросочетание совершенным.
        
        :return: True, если паросочетание совершенное, иначе False
        """
        return self._cardinality == self._order

    @property
    def cardinality(self) -> int:
        """Текущая мощность паросочетания (количество рёбер)."""
        return self._cardinality

    def is_left_covered(self, idx: int) -> bool:
        """
        Проверяет, покрыта ли левая вершина паросочетанием.
        
        :param idx: Индекс левой вершины (0 <= i < order)
        :return: True, если вершина покрыта
        """
        self._validate_idx(idx)
        return self._match_left[idx] != -1
    

    def is_right_covered(self, idx: int) -> bool:
        """
        Проверяет, покрыта ли правая вершина паросочетанием.
        
        :param idx: Индекс правой вершины (0 <= j < order)
        :return: True, если вершина покрыта
        """
        self._validate_idx(idx)
        if not (0 <= idx < self._order):
            raise IndexError(f"Right vertex index {idx} out of range [0, {self._order})")
        return self._match_right[idx] != -1
    
    def get_right_match(self, idx: int) -> int:
        """
        Возвращает индекс вершины из правой доли, сопоставленной левой вершине.
        
        :param idx: Индекс вершины в левой доле (0 <= i < order)
        :return: Индекс смежной вершины в правой доле или -1, если вершина не покрыта
        :raises IndexError: Если индекс выходит за пределы допустимого диапазона
        """
        self._validate_idx(idx)
        return self._match_left[idx]

    def get_left_match(self, idx: int) -> int:
        """
        Возвращает индекс вершины из левой доли, сопоставленной правой вершине.
        
        :param j: Индекс вершины в правой доле (0 <= j < order)
        :return: Индекс смежной вершины в левой доле или -1, если вершина не покрыта
        :raises IndexError: Если индекс выходит за пределы допустимого диапазона
        """        
        self._validate_idx(idx)
        return self._match_right[idx]

    def add_edge(self, src: int, trg: int) -> None:
        """
        Добавляет ребро в паросочетание.
        
        Требования:
        - Вершины должны быть свободны (не покрыты текущим паросочетанием)
        - Индексы должны быть в допустимом диапазоне
        
        :param src: Индекс левой вершины
        :param trg: Индекс правой вершины
        :raises ValueError: Если одна из вершин уже покрыта или индексы некорректны
        """
        self._validate_idx(src)
        self._validate_idx(trg)
            
        if self.is_left_covered(src):
            raise ValueError(ErrorMessageTemplateEnum.VERTEX_COVERED.format(src))
        if self.is_right_covered(trg):
            raise ValueError(ErrorMessageTemplateEnum.VERTEX_COVERED.format(trg))
            
        self._match_left[src] = trg
        self._match_right[trg] = src
        self._cardinality += 1

    def remove_edge(self, src: int, trg: int) -> None:
        """
        Удаляет ребро из паросочетания.
        
        Требования:
        - Ребро должно существовать в текущем паросочетании
        
        :param src: Индекс левой вершины
        :param trg: Индекс правой вершины
        :raises ValueError: Если ребро  отсутствует в паросочетании
        """
        self._validate_idx(src)
        self._validate_idx(trg)
            
        if self._match_left[src] != trg:
            raise ValueError(ErrorMessageTemplateEnum.NOT_EXISTED_EDGE.format(src, trg))
            
        self._match_left[src] = -1
        self._match_right[trg] = -1
        self._cardinality -= 1

    def get_matching(self) -> list[tuple[int, int]]:
        """
        Возвращает текущее паросочетание в виде списка пар (i, j).
        
        :return: Список рёбер паросочетания
        """
        return [(src, trg) for src, trg in enumerate(self._match_left) if trg != -1]

    def __repr__(self) -> str:
        edges = self.get_matching()
        return f"BipartiteGraphMatching(order={self._order}, matching={edges})"
    
    def _validate_idx(self, idx):
        if not isinstance(idx, int) or not (0 <= idx < self._order):
            raise IndexError(ErrorMessageEnum.WRONG_IDX)

if __name__ == "__main__":
    print("Создаём паросочетание для графа с долями мощности 5")
    matching = BipartiteGraphMatching(5)

    print("\nВыведем мощность паросочетания:")
    print(matching.cardinality)
    print(matching.is_left_covered(0))

    print("\nДобавляем рёбра (0, 1), (2, 3)")
    matching.add_edge(0, 1)
    matching.add_edge(2, 3)

    print("\nВыведем мощность паросочетания:")
    print(matching.cardinality)

    print("\nПроверяем покрыта ли вершина левой доли с индексом 0:")
    print(matching.is_left_covered(0))

    print("\nПроверяем покрыта ли вершина правой доли с индексом 0:")
    print(matching.is_right_covered(1))

    print("\nВыводим все ребра паросочетания:")
    print(matching.get_matching())

    print("\nУдаляем ребро (0, 1)")
    matching.remove_edge(0, 1)
    
    print("\nВыведем мощность паросочетания:")
    print(matching.cardinality)

    print("\nВыводим все ребра паросочетания:")
    print(matching.get_matching())


    print("\nПопытка добавить ребро с уже покрытой вершиной вызовет ошибку:")
    try:
        matching.add_edge(2, 4)
    except ValueError as ex:
        print(ex)
