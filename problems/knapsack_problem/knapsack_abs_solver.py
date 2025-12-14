from abc import ABC, abstractmethod
from collections import namedtuple

from problems.knapsack_problem.errors.constants import COSTS, WEIGHTS
from problems.knapsack_problem.errors.error_message_enum import ErrorMessageEnum
from problems.knapsack_problem.errors.error_message_template import (
    ErrorMessageTemplateEnum,
)

KnapsackSolution = namedtuple("KnapsackSolution", ["cost", "items"])


class KnapsackAbstractSolver(ABC):
    """Абстрактный класс для решения задачи о рюкзаке."""

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создает объект класса для решения задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        self._validate_params(weights, costs, weight_limit)
        self._weights = weights
        self._costs = costs
        self._weight_limit = weight_limit

    @property
    def item_cnt(self):
        """Возвращает количество предметов для рюкзака."""
        return len(self._weights)

    @property
    def weights(self):
        """Возвращает список весов предметов для рюкзака."""
        return self._weights

    @property
    def costs(self):
        """Возвращает список стоимостей предметов для рюкзака."""
        return self._costs

    @property
    def weight_limit(self):
        """Возвращает ограничение вместимости рюкзака."""
        return self._weight_limit

    @abstractmethod
    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает решение задачи о рюкзаке в виде именованного кортежа с полями:
        - cost - стоимость предметов в рюкзаке.
        - items - индексы предметов, добавленных в рюкзак.
        """
        pass

    def get_weight(self, selected_items: list[bool]) -> int:
        """Возвращает общий вес предметов, добавленных в рюкзак.

        :param selected_items: список логических значений, где для каждого предмета
        указано включен предмет в рюкзак или нет.
        """
        return sum([self.weights[i] for i in range(self.item_cnt) if selected_items[i]])

    def get_cost(self, selected_items: list[bool]) -> int:
        """Возвращает общую стоимость предметов, добавленных в рюкзак.

        :param selected_items: список логических значений, где для каждого предмета
        указано включен предмет в рюкзак или нет.
        """
        if self.get_weight(selected_items) > self.weight_limit:
            return 0
        return sum([self.costs[i] for i in range(self.item_cnt) if selected_items[i]])

    def _validate_params(
        self, weights: list[int], costs: list[int], weight_limit: int
    ) -> None:
        """Проверяет входные данные задачи о рюкзаке.

        :param weights: Список весов предметов для рюкзака.
        :param costs: Список стоимостей предметов для рюкзака.
        :param weight_limit: Ограничение вместимости рюкзака.
        :raise TypeError: Если веса или стоимости не являются списком с числовыми
        значениями, если ограничение вместимости не является целым числом.
        :raise ValueError: Если в списках присутствует нулевое или отрицательное
        значение.
        """
        self._validate_list(weights, WEIGHTS)
        self._validate_list(costs, COSTS)
        if len(weights) != len(costs):
            raise ValueError(ErrorMessageEnum.LENGTHS_NOT_EQUAL)
        if not isinstance(weight_limit, int):
            raise TypeError(ErrorMessageEnum.NOT_INT_WEIGHT_LIMIT)
        if weight_limit < 1:
            raise ValueError(ErrorMessageEnum.NOT_POS_WEIGHT_LIMIT)
        if weight_limit < min(weights):
            raise ValueError(ErrorMessageEnum.LESS_WEIGHT_LIMIT)

    def _validate_list(self, items: list[int], list_name: str) -> None:
        """Проверяет список весов или список стоимостей в зависимости от параметра list_name"""
        if not isinstance(items, list):
            raise TypeError(ErrorMessageTemplateEnum.NOT_LIST.format(list_name))
        if len(items) == 0:
            raise ValueError(ErrorMessageTemplateEnum.EMPTY_LIST.format(list_name))
        for item in items:
            if not isinstance(item, int):
                raise TypeError(ErrorMessageTemplateEnum.NOT_INT.format(list_name))
            if item < 1:
                raise ValueError(ErrorMessageTemplateEnum.NOT_POS.format(list_name))
