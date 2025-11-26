def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    n = len(matrix)
    is_valid(matrix)
    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for j in range(n):
        minor = reduced_matrix(matrix, 0, j)
        cofactor = ((-1) ** j) * matrix[0][j] * calculate_determinant(minor)
        determinant += cofactor

    return determinant

def is_valid(matrix):
    """Проверяет матрицы на квадратичность и тип int

    :param matrix: проверяемая матрица
    :raise Exception: если матрица пустая, не квадратная или содержит не int
    :return: True, если матрица валидна
    """
    if not isinstance(matrix, list) or not matrix:
        raise Exception("Матрица должна быть непустой")

    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise Exception("Матрица должна быть квадратной")
        for val in row:
            if not isinstance(val, int):
                raise Exception("Матрица должна содержать только целые числа")
    return True

def reduced_matrix(matrix, row_remove, column_remove):
    """Создаёт минор, удаляя указанную строку и столбец

    :param matrix: исходная квадратная матрица
    :param row_remove: индекс строки, которую нужно удалить
    :param col_remove: индекс столбца, который нужно удалить
    :return: новая матрица (минор)
    """
    minor = []
    for i in range(len(matrix)):
        if i == row_remove:
            continue
        row = []
        for j in range(len(matrix)):
            if j != column_remove:
                row.append(matrix[i][j])
        minor.append(row)
    return minor
def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
