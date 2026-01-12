class DoublyListNode:
    """
    Класс, описывающий узел двусвязного списка.

    Атрибуты:
        value: значение, которое хранит узел.
        prev (DoublyListNode | None): ссылка на предыдущий узел (или None, если это первый элемент).
        next (DoublyListNode | None): ссылка на следующий узел (или None, если это последний элемент).
    """

    def __init__(self, value, prev=None, next=None):
        """
        Создаёт новый узел двусвязного списка.

        Аргументы:
            value: значение узла.
            prev (DoublyListNode | None): ссылка на предыдущий узел (по умолчанию None).
            next (DoublyListNode | None): ссылка на следующий узел (по умолчанию None).
        """
        self.value = value
        self.prev = prev
        self.next = next
