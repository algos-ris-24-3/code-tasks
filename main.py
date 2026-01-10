from collections import namedtuple

from strenum import StrEnum


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


def _validate_profit_matrix(profit_matrix: list[list[int]]) -> tuple[int, int]:

    if profit_matrix is None:
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.WRONG_MATRIX)
    
    num_rows = len(profit_matrix)
    num_projects = len(profit_matrix[0])

    for row in profit_matrix:
        if not isinstance(row, list) or len(row) != num_projects:
            raise ValueError(ErrorMessages.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(ErrorMessages.WRONG_MATRIX)

    for project_idx in range(num_projects):
        for row_idx in range(num_rows):
            value = profit_matrix[row_idx][project_idx]
            if value < 0:
                raise ProfitValueError(
                    ErrorMessages.NEG_PROFIT, project_idx, row_idx
                )
            if row_idx > 0 and value < profit_matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(
                    ErrorMessages.DECR_PROFIT, project_idx, row_idx
                )
    
    return num_rows, num_projects


def _calculate_max_profit(
    profit_matrix: list[list[int]], 
    num_rows: int, 
    num_projects: int
) -> tuple[list[list[int]], int]:

    total_units = num_rows

    dp = [[0] * num_projects for _ in range(total_units + 1)]

    for j in range(num_projects):
        for i in range(total_units + 1):
            if j == 0:
                if i > 0:
                    dp[i][j] = profit_matrix[i - 1][j]
            else:
                max_profit = 0
                for k in range(i + 1):
                    if k == 0:
                        profit = dp[i][j - 1]
                    else:
                        profit = (
                            dp[i - k][j - 1] + profit_matrix[k - 1][j]
                        )
                    max_profit = max(max_profit, profit)
                dp[i][j] = max_profit
    
    max_profit = dp[total_units][num_projects - 1]
    return dp, max_profit


def _restore_distribution(
    dp: list[list[int]],
    profit_matrix: list[list[int]],
    total_units: int,
    num_projects: int
) -> list[int]:

    distribution = [0] * num_projects
    remaining_units = total_units
    
    for j in range(num_projects - 1, -1, -1):
        if j == 0:
            distribution[j] = remaining_units
            break

        best_k = 0
        best_profit = dp[remaining_units][j - 1]
        
        for k in range(1, remaining_units + 1):
            if remaining_units - k >= 0:
                profit = (
                    dp[remaining_units - k][j - 1] + profit_matrix[k - 1][j]
                )
                if profit > best_profit:
                    best_profit = profit
                    best_k = k
        
        distribution[j] = best_k
        remaining_units -= best_k
    
    return distribution


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
    num_rows, num_projects = _validate_profit_matrix(profit_matrix)
    
    dp, max_profit = _calculate_max_profit(profit_matrix, num_rows, num_projects)
    
    distribution = _restore_distribution(
        dp, profit_matrix, num_rows, num_projects
    )
    
    return Result(profit=max_profit, distribution=distribution)


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
