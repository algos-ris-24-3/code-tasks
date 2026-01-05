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
        return Result(cost = float(price_table[0][0]), path = [(0, 0)])
    
    return Result(cost = 0.0, path = [])

def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
