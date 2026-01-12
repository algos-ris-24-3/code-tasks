class ListNode:
    """
    Класс, описывающий узел (элемент) связного списка.

    Атрибуты:
        value: значение, которое хранит узел.
        next (Node | None): ссылка на следующий узел списка (или None, если это последний элемент).
    """

    def __init__(self, value, next=None):
        self.value = value
        self.next = next
