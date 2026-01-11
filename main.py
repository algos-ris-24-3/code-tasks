from collections import namedtuple

from enum import StrEnum


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках."""

    WRONG_MATRIX = (
        "Таблица прибыли от проектов не является прямоугольной "
        "матрицей с числовыми значениями"
    )
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distribution"])


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def validate_profit_matrix(profit_matrix):
    """Валидация матрицы прибыли от проектов.

    :param profit_matrix: таблица с распределением прибыли от проектов
    :raise ValueError: если таблица не является прямоугольной матрицей с
    числовыми значениями
    :raise ProfitValueError: если значение прибыли отрицательно или убывает
    с ростом инвестиций
    """
    if not isinstance(profit_matrix, list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    if not profit_matrix:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    for row in profit_matrix:
        if not isinstance(row, list):
            raise ValueError(ErrorMessages.WRONG_MATRIX)

    if not profit_matrix[0]:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    columns = len(profit_matrix[0])

    for row in profit_matrix:
        if len(row) != columns:
            raise ValueError(ErrorMessages.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, float)):
                raise ValueError(ErrorMessages.WRONG_MATRIX)

    rows = len(profit_matrix)
    for col in range(columns):
        for row in range(rows):
            profit_value = profit_matrix[row][col]
            if profit_value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, col, row)
            if row > 0 and profit_matrix[row][col] < profit_matrix[row - 1][col]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, col, row)


def get_invest_distribution(
    profit_matrix: list[list[int]],
) -> Result:
    """Рассчитывает максимально возможную прибыль и распределение инвестиций
    между несколькими проектами. Инвестиции распределяются кратными частями.

    :param profit_matrix: Таблица с распределением прибыли от проектов в
    зависимости от уровня инвестиций. Проекты указаны в столбцах, уровни
    инвестиций в строках.
    :raise ValueError: Если таблица прибыли от проектов не является
    прямоугольной матрицей с числовыми значениями.
    :raise ProfitValueError: Если значение прибыли отрицательно или убывает
    с ростом инвестиций.
    :return: именованный кортеж Result с полями:
    profit - максимально возможная прибыль от инвестиций,
    distribution - распределение инвестиций между проектами.
    """
    validate_profit_matrix(profit_matrix)

    invest_levels = len(profit_matrix)
    projects_count = len(profit_matrix[0])
    max_invest = invest_levels

    max_profit_table = [[0] * (max_invest + 1) for _ in range(projects_count + 1)]
    decisions = [[0] * (max_invest + 1) for _ in range(projects_count + 1)]

    for project in range(1, projects_count + 1):
        for amount in range(max_invest + 1):
            final_profit = 0
            best_invest = 0

            for invest in range(min(amount, invest_levels) + 1):
                if invest == 0:
                    current_profit = max_profit_table[project - 1][amount]
                else:
                    current_profit = (
                        profit_matrix[invest - 1][project - 1] + max_profit_table[project - 1][amount - invest]
                    )

                if current_profit > final_profit:
                    final_profit = current_profit
                    best_invest = invest

            max_profit_table[project][amount] = final_profit
            decisions[project][amount] = best_invest

    distribution = [0] * projects_count
    remaining = max_invest

    for project in range(projects_count, 0, -1):
        invest = decisions[project][remaining]
        distribution[project - 1] = invest
        remaining -= invest

    final_profit = max_profit_table[projects_count][max_invest]

    return Result(profit=final_profit, distribution=distribution)


def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]
    print(get_invest_distribution(profit_matrix))


if __name__ == "__main__":
    main()