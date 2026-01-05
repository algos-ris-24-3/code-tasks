from collections import namedtuple

INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])


def validate_matrix(price_table):

    if not isinstance(price_table, list):
        raise ValueError(PARAM_ERR_MSG)

    if not price_table:
        raise ValueError(PARAM_ERR_MSG)

    for row in price_table:
        if not isinstance(row, list):
            raise ValueError(PARAM_ERR_MSG)

    if not price_table[0]:
        raise ValueError(PARAM_ERR_MSG)

    for row in price_table:
        for cell in row:
            if not isinstance(cell, (int, float)):
                raise ValueError(PARAM_ERR_MSG)

    columns_count = len(price_table[0])
    for row in price_table:
        if not len(row) == columns_count:
            raise ValueError(PARAM_ERR_MSG)


def get_min_cost_path(
    price_table: list[list[float | int]],
) -> Result:
    """Возвращает путь минимальной стоимости в таблице из левого верхнего угла
    в правый нижний. Каждая ячейка в таблице имеет цену посещения. Перемещение
    из ячейки в ячейку можно производить только по горизонтали вправо или по
    вертикали вниз.
    :param price_table: Таблица с ценой посещения для каждой ячейки.
    :raise ValueError: Если таблица цен не является прямоугольной матрицей с
    числовыми значениями.
    :return: Именованный кортеж Result с полями:
    cost - стоимость минимального пути,
    path - путь, список кортежей с индексами ячеек.
    """

    validate_matrix(price_table)

    rows_count = len(price_table)
    columns_count = len(price_table[0])

    if rows_count == 1 and columns_count == 1:
        return Result(cost=float(price_table[0][0]), path=[(0, 0)])

    min_costs = [[0] * columns_count for _ in range(rows_count)]

    min_costs[0][0] = price_table[0][0]

    for row in range(1, rows_count):
        min_costs[row][0] = min_costs[row - 1][0] + price_table[row][0]

    for column in range(1, columns_count):
        min_costs[0][column] = min_costs[0][column - 1] + price_table[0][column]

    for row in range(1, rows_count):
        for column in range(1, columns_count):
            min_costs[row][column] = price_table[row][column] + min(
                min_costs[row - 1][column], min_costs[row][column - 1]
            )

    path_result = []

    current_row = rows_count - 1

    current_column = columns_count - 1

    path_result.append((current_row, current_column))

    while current_row > 0 or current_column > 0:
        if current_row == 0:
            current_column -= 1
        elif current_column == 0:
            current_row -= 1
        else:
            if (
                min_costs[current_row - 1][current_column]
                < min_costs[current_row][current_column - 1]
            ):
                current_row -= 1
            else:
                current_column -= 1

        path_result.append((current_row, current_column))

    path_result.reverse()

    return Result(
        cost=float(min_costs[rows_count - 1][columns_count - 1]), path=path_result
    )


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
