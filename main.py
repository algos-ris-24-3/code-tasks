def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """

    if is_valid_matrix(matrix):
        return calculate_determinant_bet(matrix)

def calculate_determinant_bet(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    
    det = 0
    for idx, item in enumerate(matrix[0]):
        det += item * (-1)**idx * calculate_determinant_bet(get_reduced_matrix(matrix, 0, idx))

    return det

def get_reduced_matrix(matrix, row_idx, col_idx):
    """Уменьшает ранг матрицы на один, убирая строку и столбец по их индексу

    :param matrix: целочисленная квадратная матрица
    :param row_idx: индекс строки для удаления
    :param col_idx: индекс столбца для удаления
    :return: матрица с уменьшенным рангом
    """
    reduced_matrix = []
    
    for i in range(len(matrix)):
        if i != row_idx:
            new_row = []
            for j in range(len(matrix)):
                if j != col_idx:
                    new_row.append(matrix[i][j])
            reduced_matrix.append(new_row)
    return reduced_matrix


def is_valid_matrix(matrix: any) -> bool:
    """Проверяет матрицу на квадратность и тип int."""

    if not isinstance(matrix, list) or not matrix:
        raise Exception("Матрица должна быть непустым списком списков.")

    n = len(matrix)

    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise Exception("Матрица должна быть квадратной n*n.")
        for val in row:
            if not isinstance(val, int):
                raise Exception("Матрица должна содержать только целые числа.")

    return True


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
