def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """
    checking_conditions(matrix)

    n = len(matrix)

    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] ** 2 - matrix[0][1] * matrix[1][0]
    
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]

    return calculate_tridiagonal_det(n, a, b, c)

def calculate_tridiagonal_det(n: int, a: int, b: int, c: int) -> int:
    """Вычисляет определитель трехдиагональной матрицы с постоянными диагоналями.
    :param n: размер матрицы
    :param a: значение на главной диагонали
    :param b: значение на верхней диагонали
    :param c: значение на нижней диагонали
    
    :return: значение определителя
    """
    if n == 1:
        return a
    elif n == 2:
        return a * a - b * c
    
    return a * calculate_tridiagonal_det(n - 1, a, b, c) - b * c * calculate_tridiagonal_det(n - 2, a, b, c)

def checking_conditions(matrix):
    """Проверяет, является ли матрица трехдиагональной с постоянными значениями на диагоналях.
    :param matrix: матрица для проверки условий трехдиагональности
    
    :return: None если проверки пройдены успешно
    """
    n = len(matrix)

    if not matrix or not isinstance(matrix, list):
        return Exception("Матрицы нет")
    
    for i in range(n):
        if len(matrix[i]) != n:
            raise Exception("Матрица должна быть квадратной")
            
    main_diag_value = matrix[0][0]
    
    upper_diag_value = None
    lower_diag_value = None
    
    if n >= 2:
        upper_diag_value = matrix[0][1]
        lower_diag_value = matrix[1][0]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                if matrix[i][j] != main_diag_value:
                    raise Exception("Элементы главной строки не одинаковые")
            elif j == i + 1:
                if n >= 2 and matrix[i][j] != upper_diag_value:
                    raise Exception("Элементы строки над главной не одинаковые")
            elif i == j + 1:
                if n >= 2 and matrix[i][j] != lower_diag_value:
                    raise Exception("Элементы строки под главной не одинаковые")
            else:
                if matrix[i][j] != 0:
                    raise Exception("Элементы остальных строк не нулевые")

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()