def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """

    validate_matrix(matrix)

    matrix_order = len(matrix)

    if matrix_order == 1:
        return matrix[0][0]

    main_diagonal, upper_diagonal, lower_diagonal = (
        matrix[0][0],
        matrix[0][1],
        matrix[1][0],
    )

    return recursion_determinant(
        matrix_order, main_diagonal, upper_diagonal, lower_diagonal
    )


def recursion_determinant(matrix_order, main_diagonal, upper_diagonal, lower_diagonal):
    if matrix_order == 1:
        return main_diagonal

    if matrix_order == 2:
        return main_diagonal * main_diagonal - upper_diagonal * lower_diagonal

    return main_diagonal * recursion_determinant(
        matrix_order - 1, main_diagonal, upper_diagonal, lower_diagonal
    ) - upper_diagonal * lower_diagonal * recursion_determinant(
        matrix_order - 2, main_diagonal, upper_diagonal, lower_diagonal
    )


def validate_matrix(matrix: list[list[int]]):
    if matrix is None:
        raise Exception("Матрица не может быть пустой")

    matrix_order = len(matrix)

    if matrix_order == 0:
        raise Exception("Матрица не может быть пустой")

    for row in matrix:
        if len(row) != matrix_order:
            raise Exception("Матрица должна быть квадратной")

    for row in range(matrix_order):
        for column in range(matrix_order):
            if abs(row - column) <= 1:
                continue
            if matrix[row][column] != 0:
                raise Exception("Ненулевой элемент вне диагоналях матрицы")

    main_diagonal = matrix[0][0]

    if matrix_order == 1:
        return

    # i - строка и столбец одновременно
    for i in range(1, matrix_order):
        if matrix[i][i] != main_diagonal:
            raise Exception("Неверное значение на главной диагонали матрицы")

    upper_diagonal = matrix[0][1]
    lower_diagonal = matrix[1][0]

    for i in range(matrix_order - 1):
        if matrix[i][i + 1] != upper_diagonal:
            raise Exception("Неверное значение на верхней диагонали матрицы")
    for i in range(1, matrix_order):
        if matrix[i][i - 1] != lower_diagonal:
            raise Exception("Неверное значение на нижней диагонали матрицы")


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]

    try:
        validate_matrix(matrix)
        print("Матрица корректна")
    except Exception as error:
        print(f"Ошибка валидации: {error}")
        exit()

    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
