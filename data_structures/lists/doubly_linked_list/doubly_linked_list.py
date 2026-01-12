from data_structures.lists.base_list import BaseList
from data_structures.lists.doubly_linked_list.doubly_list_node import DoublyListNode


class DoublyLinkedList(BaseList):
    """
    Реализация двусвязного списка.

    Атрибуты:
        head (DoublyListNode | None): ссылка на первый элемент списка.
        tail (DoublyListNode | None): ссылка на последний элемент списка.
        size (int): количество элементов в списке.

    Поддерживаемые операции:
        - append(value): добавить элемент в конец
        - appendleft(value): добавить элемент в начало
        - insert(index, value): вставить элемент по индексу
        - remove(value): удалить первый найденный элемент
        - pop(): удалить последний элемент и вернуть его
        - popleft(): удалить первый элемент и вернуть его
        - index(value): вернуть индекс первого найденного элемента
        - __str__(): вернуть строковое представление двусвязного списка
        - __len__(): вернуть количество элементов
        - __iter__(): прямой обход
        - __reversed__(): обратный обход
    """

    def __init__(self):
        """Создаёт пустой двусвязный список."""
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        """Добавляет элемент в конец списка."""
        pass

    def appendleft(self, value):
        """Добавляет элемент в начало списка."""
        pass

    def insert(self, index, value):
        """Вставляет элемент по указанному индексу (0 ≤ index ≤ len)."""
        pass

    def remove(self, value):
        """Удаляет первый элемент с указанным значением."""
        pass

    def pop(self):
        """Удаляет и возвращает последний элемент."""
        pass

    def popleft(self):
        """Удаляет и возвращает первый элемент."""
        pass

    def index(self, value):
        """Возвращает индекс первого элемента с указанным значением или None."""
        pass

    def __str__(self) -> str:
        """Возвращает строковое представление двусвязного списка."""
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " <-> ".join(values)

    def __len__(self):
        """Возвращает количество элементов в списке."""
        return self.size

    def __iter__(self):
        """Итерация по элементам списка слева направо."""
        pass

    def __reversed__(self):
        """Итерация по элементам списка справа налево."""
        pass


if __name__ == "__main__":
    dll = DoublyLinkedList()

    dll.append(10)
    dll.append(20)
    dll.append(30)
    print("После добавления:", dll)

    dll.insert(0, 5)
    print("После вставки в начало:", dll)

    dll.insert(2, 15)
    print("После вставки в середину:", dll)

    dll.remove(20)
    print("После удаления 20:", dll)

    idx = dll.index(30)
    print(f"Индекс элемента 30: {idx}")

    print("Размер списка:", len(dll))

    print("Элементы списка:", [x for x in dll])

    print("Обратный обход:", [x for x in reversed(dll)])
