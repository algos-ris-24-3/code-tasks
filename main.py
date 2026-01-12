from collections import namedtuple


INF = float("inf")
PARAM_ERR_MSG = "Таблица цен не является прямоугольной матрицей с числовыми значениями"

Result = namedtuple("Result", ["cost", "path"])


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
    row_count = len(price_table) 
    col_count = len(price_table[0])

    if row_count == 0:
        raise ValueError(PARAM_ERR_MSG)
        
    for i in range(row_count):
        if len(price_table[i]) != col_count:
            raise ValueError(PARAM_ERR_MSG)
    
    for i in range(row_count):
        for j in range(col_count):
            value = price_table[i][j]
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError(PARAM_ERR_MSG)

    if price_table[0][0] is None or price_table[row_count - 1][col_count - 1] is None:
        return Result(cost=None, path=None)

    path_cost = [[INF] * (col_count + 1) for _ in range(row_count + 1)]

    path_cost[1][1] = price_table[0][0]

    for j in range(2, col_count + 1):
        if path_cost[1][j - 1] == INF or price_table[0][j - 1] is None:
            path_cost[1][j] = INF
        else:
            path_cost[1][j] = path_cost[1][j - 1] + price_table[0][j - 1]

    for i in range(2, row_count + 1):
        if path_cost[i - 1][1] == INF or price_table[i - 1][0] is None:
            path_cost[i][1] = INF
        else:
            path_cost[i][1] = path_cost[i - 1][1] + price_table[i - 1][0]

    for row_idx in range(1, row_count + 1):
        for col_idx in range(1, col_count + 1):
            if row_idx == 1 and col_idx == 1:
                continue
            else:
                price_table_value = price_table[row_idx - 1][col_idx - 1]
                if price_table_value is None:
                    path_cost[row_idx][col_idx] = INF
                else:
                    min_cost = min(path_cost[row_idx - 1][col_idx], path_cost[row_idx][col_idx - 1])
                    if min_cost == INF:
                        path_cost[row_idx][col_idx] = INF
                    else:
                        path_cost[row_idx][col_idx] = min_cost + price_table_value
                
    min_cost = path_cost[row_count][col_count]
    
    if min_cost != INF:
        path = []
        i, j = row_count, col_count
        
        while i > 1 or j > 1:
            path.append((i - 1, j - 1))
            
            if i > 1 and j > 1:
                if path_cost[i - 1][j] <= path_cost[i][j - 1]:
                    i -= 1
                else:
                    j -= 1
            elif i > 1:
                i -= 1
            else:
                j -= 1
        
        path.append((0, 0))
        path.reverse()
        
        return Result(cost=min_cost, path=tuple(path))
    else:
        return Result(cost=None, path=None)

def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
