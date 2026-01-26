from collections import namedtuple
from assignment_problem.errors.error_message_enum import ErrorMessageEnum
from assignment_problem.hungarian import hungarian


AssignmentSolution = namedtuple("AssignmentSolution", ["cost", "assignments"])

def get_assignments(cost_matrix: list[list[int | float]]) -> AssignmentSolution:
    """
    Решает задачу о назначениях с использованием венгерского алгоритма.

    Задача заключается в нахождении совершенного паросочетания "исполнителей" (строки)
    и "задач" (столбцы), минимизирующей суммарную стоимость выполнения.
    Предполагается, что входная матрица квадратная (число исполнителей равно числу задач).

    :param cost_matrix: Квадратная матрица стоимостей размера n×n,
                        где cost_matrix[i][j] — стоимость назначения i-го исполнителя на j-ю задачу.
    :return: Объект AssignmentSolution, содержащий минимальную суммарную стоимость
             и список пар (i, j), представляющих оптимальные назначения.
    :raises ValueError: Если матрица некорректна (неквадратная, пустая, содержит недопустимые значения).
    """
    _validate_matrix(cost_matrix)
    matching = hungarian(cost_matrix)
    total_cost = 0
    assignments = matching.get_matching()
    for row_idx, col_idx in assignments:
        total_cost += cost_matrix[row_idx][col_idx]

    return AssignmentSolution(total_cost, assignments)


def _validate_matrix(matrix: list[list[int | float]]) -> None:
    if (
        not matrix
        or not isinstance(matrix, list)
        or not matrix[0]
        or not isinstance(matrix[0], list)
    ):
        raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
    row_cnt = len(matrix[0])
    for row in matrix:
        if len(row) != row_cnt:
            raise ValueError(ErrorMessageEnum.WRONG_MATRIX)
        for value in row:
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(ErrorMessageEnum.WRONG_MATRIX)


if __name__ == "__main__":
    matrix = [
        [6, 7, 8, 14, 7],
        [8, 14, 6, 9, 7],
        [14, 14, 13, 9, 11],
        [5, 12, 10, 9, 14],
        [6, 10, 8, 10, 15],
    ]
    print("Исходная матрица")
    for row in matrix:
        print(row)

    matching = hungarian(matrix)
    
    result = get_assignments(matrix)
    print("\nРешение задачи о назначениях")
    print(f"Стоимость назначения: {result.cost}")
    print("Назначения: ")
    for assignment in result.assignments:
        print(assignment)
