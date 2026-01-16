from data_structures.lists.base_list import BaseList
from data_structures.lists.doubly_linked_list.doubly_list_node import DoublyListNode


class DoublyLinkedList(BaseList):
    def __init__(self):
        """Создаёт пустой двусвязный список."""
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        """Добавляет элемент в конец списка."""
        new_node = DoublyListNode(value, prev=self.tail, next=None)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def appendleft(self, value):
        """Добавляет элемент в начало списка."""
        new_node = DoublyListNode(value, prev=None, next=self.head)

        if self.head is None: 
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def insert(self, index, value):
        """Вставляет элемент по указанному индексу (0 ≤ index ≤ len)."""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        if index == self.size:
            self.append(value)
            return

        if index == 0:
            self.appendleft(value)
            return

        if index <= self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - index):
                current = current.prev

        prev_node = current.prev
        new_node = DoublyListNode(value, prev=prev_node, next=current)

        prev_node.next = new_node
        current.prev = new_node

        self.size += 1

    def remove(self, value):
        """Удаляет первый элемент с указанным значением."""
        current = self.head
        while current:
            if current.value == value:
                prev_node = current.prev
                next_node = current.next

                if prev_node is None: 
                    self.head = next_node
                else:
                    prev_node.next = next_node

                if next_node is None:  
                    self.tail = prev_node
                else:
                    next_node.prev = prev_node

                self.size -= 1
                return

            current = current.next

        raise ValueError("Value not found")

    def pop(self):
        """Удаляет и возвращает последний элемент."""
        if self.tail is None:
            raise IndexError("pop from empty list")

        node = self.tail
        value = node.value

        new_tail = node.prev
        if new_tail is None: 
            self.head = None
            self.tail = None
        else:
            new_tail.next = None
            self.tail = new_tail

        self.size -= 1
        return value

    def popleft(self):
        """Удаляет и возвращает первый элемент."""
        if self.head is None:
            raise IndexError("popleft from empty list")

        node = self.head
        value = node.value

        new_head = node.next
        if new_head is None:
            self.head = None
            self.tail = None
        else:
            new_head.prev = None
            self.head = new_head

        self.size -= 1
        return value

    def index(self, value):
        """Возвращает индекс первого элемента с указанным значением или None."""
        i = 0
        current = self.head
        while current:
            if current.value == value:
                return i
            current = current.next
            i += 1

        return None

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
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __reversed__(self):
        """Итерация по элементам списка справа налево."""
        current = self.tail
        while current:
            yield current.value
            current = current.prev


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
