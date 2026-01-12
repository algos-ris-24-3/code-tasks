import unittest

from data_structures.lists.doubly_linked_list.doubly_linked_list import DoublyLinkedList
from tests.data_structures.lists.test_baselist import TestBaseList


class TestDoublyLinkedList(unittest.TestCase, TestBaseList):
    """Набор тестов для класса DoublyLinkedList."""

    def create_list(self):
        """Вернёт DoublyLinkedList"""
        return DoublyLinkedList()

    def test_appendleft_adds_element_to_head(self):
        """appendleft должен поместить элемент в начало списка."""
        lst = self.create_list()
        lst.append(10)

        lst.appendleft(5)

        self.assertEqual(list(lst), [5, 10])

    def test_pop_removes_last_element(self):
        """pop возвращает и удаляет последний элемент."""
        lst = self.create_list()
        lst.append(1)
        lst.append(2)

        value = lst.pop()

        self.assertEqual(value, 2)
        self.assertEqual(list(lst), [1])
        self.assertEqual(len(lst), 1)

    def test_pop_on_empty_list_raises(self):
        """pop на пустом списке должен вызывать IndexError."""
        lst = self.create_list()

        with self.assertRaises(IndexError):
            lst.pop()

    def test_popleft_removes_first_element(self):
        """popleft возвращает и удаляет первый элемент."""
        lst = self.create_list()
        lst.append(1)
        lst.append(2)

        value = lst.popleft()

        self.assertEqual(value, 1)
        self.assertEqual(list(lst), [2])
        self.assertEqual(len(lst), 1)

    def test_popleft_on_empty_list_raises(self):
        """popleft на пустом списке должен вызывать IndexError."""
        lst = self.create_list()

        with self.assertRaises(IndexError):
            lst.popleft()

    def test_bidirectional_iteration(self):
        """Если поддерживается reversed, reversed(lst) должен вернуть элементы в обратном порядке."""
        lst = self.create_list()
        lst.append(1)
        lst.append(2)
        lst.append(3)

        self.assertEqual(list(reversed(lst)), [3, 2, 1])

    def test_internal_links_consistent(self):
        """
        Если у списка есть head/tail и у узлов prev/next — проверяем согласованность внутренних связей.
        Тест пропускается, если эти атрибуты не доступны.
        """
        lst = self.create_list()
        lst.append(1)
        lst.append(2)
        lst.append(3)

        head = lst.head
        tail = lst.tail

        forward = []
        cur = head
        while cur is not None:
            forward.append(cur.value)
            cur = getattr(cur, "next", None)

        self.assertEqual(forward, [1, 2, 3])

        backward = []
        cur = tail
        while cur is not None:
            backward.append(cur.value)
            cur = getattr(cur, "prev", None)

        self.assertEqual(backward, [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
