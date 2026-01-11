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


Result = namedtuple("Result", ["profit", "distributions"])


class ProfitValueError(Exception):
    def __init__(self, message, project_idx, row_idx):
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def validate_matrix(profit_matrix: list[list[int]]) -> None:
    """Проверяет корректность входной матрицы.

    :raise ValueError: Если структура матрицы неверна.
    :raise ProfitValueError: Если значения отрицательные или убывают.
    """
    if not profit_matrix or not isinstance(profit_matrix, list):
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    rows_count = len(profit_matrix)
    cols_count = len(profit_matrix[0]) if rows_count > 0 else 0

    if cols_count == 0:
        raise ValueError(ErrorMessages.WRONG_MATRIX)

    for r_idx, row in enumerate(profit_matrix):
        if not isinstance(row, list) or len(row) != cols_count:
            raise ValueError(ErrorMessages.WRONG_MATRIX)

        for c_idx, val in enumerate(row):
            if not isinstance(val, (int, float)):
                raise ValueError(ErrorMessages.WRONG_MATRIX)

            if val < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, c_idx, r_idx)

            if r_idx > 0:
                prev_val = profit_matrix[r_idx - 1][c_idx]
                if val < prev_val:
                    raise ProfitValueError(ErrorMessages.DECR_PROFIT, c_idx, r_idx)


def get_profit(profit_matrix: list[list[int]], project_idx: int, investment: int) -> int:
    """Возвращает прибыль от проекта при заданном уровне инвестиций.

    :param project_idx: Индекс проекта (столбец).
    :param investment: Размер инвестиций.
    """
    if investment == 0:
        return 0

    return profit_matrix[investment - 1][project_idx]


def reconstruct_paths(choices: list[list[list[int]]], projects_num: int, cap: int) -> list[list[int]]:
    """Рекурсивно восстанавливает все варианты распределения инвестиций.

    :param choices: Таблица выбора оптимальных вложений.
    :param projects_num: Текущий индекс проекта.
    :param cap: Текущий остаток капитала.
    :return: Матрица с распределением инвестиций.
    """
    if projects_num == 0:
        return [[]]

    paths = []

    possible_investments = choices[projects_num][cap]
    
    for invest in possible_investments:
        remaining_cap = cap - invest

        prev_paths = reconstruct_paths(choices, projects_num - 1, remaining_cap)
        
        for path in prev_paths:
            paths.append(path + [invest])
            
    return paths


def get_invest_distributions(
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
    distributions - списком со всеми вариантами распределения инвестиций между
    проектами, обеспечивающими максимальную прибыль.
    """
    validate_matrix(profit_matrix)

    max_capital = len(profit_matrix)
    num_projects = len(profit_matrix[0])

    max_profits = [[0] * (max_capital + 1) for _ in range(num_projects + 1)]
    
    choices = [[[] for _ in range(max_capital + 1)] for _ in range(num_projects + 1)]

    for p in range(1, num_projects + 1):
        for c in range(max_capital + 1):
            
            max_val = -1
            best_inv_list = []

            for k in range(c + 1):
                current_proj_profit = get_profit(profit_matrix, p - 1, k)
                
                remaining_cap = c - k
                prev_profit = max_profits[p - 1][remaining_cap]
                
                total_profit = prev_profit + current_proj_profit
                
                if total_profit > max_val:
                    max_val = total_profit
                    best_inv_list = [k]
                elif total_profit == max_val:
                    best_inv_list.append(k)
            
            max_profits[p][c] = max_val
            choices[p][c] = best_inv_list

    max_total_profit = max_profits[num_projects][max_capital]
    
    all_distributions = reconstruct_paths(choices, num_projects, max_capital)

    return Result(profit=max_total_profit, distributions=all_distributions)


def main():
    profit_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()