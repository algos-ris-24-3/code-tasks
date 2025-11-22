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

    return a * get_tridiagonal_determinant(get_reduced_matrix(matrix)) - b * c * get_tridiagonal_determinant(get_reduced_matrix(get_reduced_matrix(matrix)))

def get_reduced_matrix(matrix, remove_row=0, remove_col=0) -> list[list[int]]:
    """Уменьшает порядок квадратной матрицы на единицу путем удаления указанных строки и столбца.
    :param matrix: исходная квадратная матрица для уменьшения
    :param remove_row: индекс строки для удаления, по умолчанию 0
    :param remove_col: индекс столбца для удаления, по умолчанию 0  
    
    :return: матрица уменьшенного порядка (n-1) x (n-1)
    """
    n = len(matrix)
    reduced_matrix = []
    
    for i in range(n):
        if i == remove_row:
            continue
        
        new_row = []
        for j in range(n):
            if j == remove_col:
                continue
            new_row.append(matrix[i][j])
        
        reduced_matrix.append(new_row)
    
    return reduced_matrix

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