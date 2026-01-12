from abc import ABC, abstractmethod
from collections import namedtuple

from problems.tsp_problem.errors.error_message_enum import ErrorMessageEnum

TspSolution = namedtuple("TspSolution", ["distance", "path"])
NullableNumber = int | float | None


class AbstractTspSolver(ABC):
    """Абстрактный класс для решения задачи коммивояжера."""

    def __init__(self, dist_matrix: list[list[NullableNumber]]) -> None:
        """Создает объект класса для решения задачи коммивояжера.

        :param dist_matrix: Матрица расстояний.
        :raise TypeError: Если таблица расстояний не является прямоугольной
        матрицей с числовыми значениями.
        :raise ValueError: Если в матрице присутствует отрицательное значение.
        """
        self._validate_params(dist_matrix)
        self._dist_matrix = dist_matrix

    @property
    def order(self):
        """Возвращает порядок матрицы расстояний."""
        return len(self._dist_matrix)

    @abstractmethod
    def get_tsp_solution(self) -> TspSolution:
        """Возвращает решение задачи коммивояжера в виде именованного кортежа с полями:
        - distance - кратчайшее расстояние,
        - path - список с индексами вершин на кратчайшем маршруте.
        """
        pass

    def get_distance(
        self, dist_matrix: list[list[NullableNumber]], path: list[int]
    ) -> float:
        """Возвращает суммарное расстояние указанного маршрута.

        :param dist_matrix: Матрица расстояний.
        :param path: Список с индексами вершин на маршруте.
        """
        distance = 0
        for i in range(1, len(path)):
            src = path[i - 1]
            trg = path[i]
            distance += dist_matrix[src][trg]
        return distance

    def _validate_params(self, matrix: list[list[NullableNumber]]) -> None:
        """Проверяет входные данные задачи коммивояжера.

        :param dist_matrix: Матрица расстояний.
        :raise TypeError: Если таблица расстояний не является прямоугольной
        матрицей с числовыми значениями.
        :raise ValueError: Если в матрице присутствует отрицательное значение.
        """
        if (
            not matrix
            or not isinstance(matrix, list)
            or not matrix[0]
            or not isinstance(matrix[0], list)
        ):
            raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
        row_len = len(matrix[0])
        if row_len != len(matrix):
            raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
        for row_idx in range(len(matrix)):
            if len(matrix[row_idx]) != row_len:
                raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
            for col_idx in range(row_len):
                if not isinstance(matrix[row_idx][col_idx], NullableNumber):
                    raise TypeError(ErrorMessageEnum.WRONG_MATRIX)
                if matrix[row_idx][col_idx] and matrix[row_idx][col_idx] < 0:
                    raise ValueError(ErrorMessageEnum.NEG_VALUE, col_idx, row_idx)
