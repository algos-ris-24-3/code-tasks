from abc import ABC, abstractmethod
from typing import Any, Iterator


class BaseList(ABC):
    """
    Абстрактный базовый класс для списковых структур данных.

    Определяет общий интерфейс, который должны реализовывать
    все конкретные классы списков (односвязный, двусвязный и т.д.).

    Методы этого класса задают контракт:
    - добавление элементов,
    - вставка по индексу,
    - удаление,
    - поиск,
    - итерация и представление в виде строки.
    """

    @abstractmethod
    def append(self, value: Any) -> None:
        """
        Добавить элемент в конец списка.

        :param value: значение, которое нужно добавить
        """
        pass

    @abstractmethod
    def insert(self, index: int, value: Any) -> None:
        """
        Вставить элемент в список по индексу.

        :param index: позиция вставки (0-based)
        :param value: значение для вставки
        :raises IndexError: если индекс вне допустимого диапазона
        """
        pass

    @abstractmethod
    def remove(self, value: Any) -> None:
        """
        Удалить первое вхождение элемента из списка.

        :param value: значение для удаления
        :raises ValueError: если элемента нет в списке
        """
        pass

    @abstractmethod
    def index(self, value: Any) -> int:
        """
        Найти индекс первого вхождения элемента.

        :param value: искомое значение
        :return: индекс найденного элемента
        :raises ValueError: если элемента нет в списке
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """
        Вернуть количество элементов в списке.

        :return: длина списка
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """
        Итератор по элементам списка.

        :return: итератор значений
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Текстовое представление списка.

        :return: строка вида [elem1, elem2, ...]
        """
        pass
