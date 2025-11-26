def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """

    if tridiagonal_determinant_validation(matrix):
        n = len(matrix)
        a = matrix[0][0]
        if n == 1:
            return a
        else:
            b = matrix[0][1]
            c = matrix[1][0]
            return get_tridiagonal_determinant_without_matrix(a, b, c, n)
    else:
        raise Exception(
            "Определитель не может быть вычислен из-за некорректности входных данных"
        )


def tridiagonal_determinant_validation(matrix: list[list[int]]) -> bool:
    """Определяет корректность введенной трехдиагональной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: True если все проверки пройдены успешно.
    :raises Exception: при обнаружении некорректных данных в матрице.
    """

    if not matrix:
        raise Exception("Матрица пуста")

    n = len(matrix)

    for _, row in enumerate(matrix):
        if len(row) != n:
            raise Exception("Матрица не квадратная")

    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and matrix[i][j] != 0:
                raise Exception("Матрица не является трехдиагональной")

    main_diag_number = matrix[0][0]
    for i in range(1, n):
        if matrix[i][i] != main_diag_number:
            raise Exception("Элементы главной диагонали не совпадают")

    if n > 1:

        upper_diag_number = matrix[0][1]
        for i in range(n - 1):
            if matrix[i][i + 1] != upper_diag_number:
                raise Exception("Элементы верхней диагонали не совпадают")

        lower_diag_number = matrix[1][0]
        for i in range(1, n):
            if matrix[i][i - 1] != lower_diag_number:
                raise Exception("Элементы нижней диагонали не совпадают")

    return True


def get_tridiagonal_determinant_without_matrix(a, b, c, n) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы из значений трех диагоналей.
    :param a: элемент главной диагонали трехдиагональной квадратной матрицы.
    :param b: элемент верхней диагонали трехдиагональной квадратной матрицы.
    :param c: элемент нижней диагонали трехдиагональной квадратной матрицы.
    :param n: размерность трехдиагональной квадратной матрицы.

    :return: значение определителя.
    """
    if n == 1:
        return a
    elif n == 2:
        return a**2 - b * c
    return a * get_tridiagonal_determinant_without_matrix(
        a, b, c, n - 1
    ) - b * c * get_tridiagonal_determinant_without_matrix(a, b, c, n - 2)


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
