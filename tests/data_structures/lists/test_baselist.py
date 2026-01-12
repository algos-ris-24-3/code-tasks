from abc import ABC, abstractmethod

from data_structures.lists.base_list import BaseList


class TestBaseList(ABC):
    """Набор тестов для классов наследующих от BaseList."""

    @abstractmethod
    def create_list(self):
        """Вернёт новый пустой список нужного типа"""
        pass

    def test_list_inherits_base_list(self):
        """Проверяем, что список является наследником BaseList"""
        self.assertTrue(issubclass(type(self.create_list()), BaseList))

    def test_empty_init(self):
        """Новый список пустой: длина 0, head = None."""
        lst = self.create_list()

        self.assertEqual(len(lst), 0)
        self.assertIsNone(lst.head)

    def test_append_one(self):
        """append добавляет элемент в конец, список из одного элемента работает корректно."""
        lst = self.create_list()
        lst.append(10)

        self.assertEqual(len(lst), 1)
        self.assertEqual(list(lst), [10])

    def test_append_many(self):
        """append несколько раз сохраняет порядок элементов."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        self.assertEqual(len(lst), 3)
        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_head(self):
        """insert в начало (index=0)."""
        lst = self.create_list()
        lst.append(1)

        lst.insert(0, 0)

        self.assertEqual(list(lst), [0, 1])

    def test_insert_tail(self):
        """insert в конец (index=len)."""
        lst = self.create_list()
        lst.append(1)

        lst.insert(1, 2)

        self.assertEqual(list(lst), [1, 2])

    def test_insert_middle(self):
        """insert вставляет элемент в середину списка."""
        lst = self.create_list()
        for val in [1, 3]:
            lst.append(val)

        lst.insert(1, 2)

        self.assertEqual(list(lst), [1, 2, 3])

    def test_insert_invalid_index(self):
        """insert с некорректным индексом выбрасывает IndexError."""
        lst = self.create_list()

        with self.assertRaises(IndexError):
            lst.insert(5, 10)

    def test_insert_negative_index(self):
        """insert с отрицательным индексом выбрасывает IndexError."""
        lst = self.create_list()
        lst.append(1)

        with self.assertRaises(IndexError):
            lst.insert(-1, 99)

    def test_remove_head(self):
        """remove удаляет первый элемент (head) корректно."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        lst.remove(1)

        self.assertEqual(list(lst), [2, 3])

    def test_remove_tail(self):
        """remove удаляет последний элемент (tail) корректно."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        lst.remove(3)

        self.assertEqual(list(lst), [1, 2])

    def test_remove_middle(self):
        """remove удаляет элемент из середины списка."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        lst.remove(2)

        self.assertEqual(list(lst), [1, 3])

    def test_remove_not_found(self):
        """remove несуществующего элемента выбрасывает ValueError."""
        lst = self.create_list()
        lst.append(1)

        with self.assertRaises(ValueError):
            lst.remove(99)

    def test_index_found(self):
        """index возвращает индекс первого найденного элемента."""
        lst = self.create_list()

        for val in ["a", "b", "c"]:
            lst.append(val)

        self.assertEqual(lst.index("b"), 1)

    def test_index_not_found(self):
        """index возвращает None, если элемента нет."""
        lst = self.create_list()
        lst.append("a")

        self.assertIsNone(lst.index("z"))

    def test_index_multiple_occurrences(self):
        """index возвращает индекс первого вхождения, если элемент встречается несколько раз."""
        lst = self.create_list()
        for val in [1, 2, 2, 3]:
            lst.append(val)

        self.assertEqual(lst.index(2), 1)

    def test_iteration(self):
        """Итерация по списку возвращает элементы в правильном порядке."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        collected = [x for x in lst]

        self.assertEqual(collected, [1, 2, 3])

    def test_size_updates(self):
        """Поле size корректно обновляется при добавлении и удалении элементов."""
        lst = self.create_list()
        self.assertEqual(len(lst), 0)
        lst.append(1)
        self.assertEqual(len(lst), 1)
        lst.append(2)
        self.assertEqual(len(lst), 2)
        lst.remove(1)
        self.assertEqual(len(lst), 1)
        lst.remove(2)
        self.assertEqual(len(lst), 0)

    def test_str_repr(self):
        """__str__ возвращает строку с элементами списка."""
        lst = self.create_list()
        for val in [1, 2, 3]:
            lst.append(val)

        s = str(lst)

        self.assertIn("1", s)
        self.assertIn("2", s)
        self.assertIn("3", s)
