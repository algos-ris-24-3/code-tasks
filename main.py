def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель трехдиагональной целочисленной квадратной матрицы.
    :param matrix: целочисленная трехдиагональная квадратная матрица.

    :return: значение определителя.
    """

    validate_matrix(matrix)

    n=len(matrix)

    if n == 1:
        return matrix[0][0]

    a, b, c = matrix[0][0], matrix[0][1], matrix[1][0]

    return recursion_determinant(n, a, b, c)
    

def recursion_determinant(n, a, b, c):
    # Базовый случай: Матрица 1x1 (1 элемент)
    if n == 1:
        return a

    # Базовый случай: Матрица 2x2 (4 элемента)
    if n == 2:
        return a * a - b * c
    
    return (a * recursion_determinant(n - 1, a, b, c) - b * c * recursion_determinant(n - 2, a, b, c))

 
def validate_matrix(matrix: list[list[int]]):
    #Проверка на None
    if matrix is None:
        raise Exception("Матрица не может быть пустой")
    
    n = len(matrix)

    #Проверка на пустой список
    if n == 0:
        raise Exception("Матрица не может быть пустой")
    
    #Проверка на квадратную матрицу
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")
    
    #Проверка элементов вне диагоналей
    for i in range(n):
        for y in range(n):
            if abs(i-y) <= 1:
                continue
            if matrix[i][y] != 0:
                raise Exception("Ненулевой элемент вне диагоналях матрицы")
    
    #Проверка элементов на диагоналях
    a = matrix[0][0] #главная диагональ

    if n == 1:
        return

    for i in range(1, n):
        if matrix[i][i] != a:
            raise Exception("Неверное значение на главной диагонали матрицы")
        
    b = matrix[0][1] #верхняя диагональ
    c = matrix[1][0] #нижняя диагональ

    for i in range(n-1):
        if matrix[i][i+1] != b:
            raise Exception("Неверное значение на верхней диагонали матрицы")
    for i in range(1, n):
        if matrix[i][i-1] != c:
            raise Exception("Неверное значение на нижней диагонали матрицы")

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]

    try:
        validate_matrix(matrix)
        print("Матрица корректна")
    except Exception as error:
        print(f"Ошибка валидации: {error}")

    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
