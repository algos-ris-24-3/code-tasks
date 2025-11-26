def check_matrix(matrix: list[list[int]]):
    """Проверяет, является ли матрица квадратной
    
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :param matrix: целочисленная квадратная матрица
    """
    #Проверка матрицы на null
    if not matrix:
        raise Exception("Матрица не может быть пустой")
    #Проверка матрицы на то, что она - list
    if not isinstance(matrix, list):
        raise Exception("Матрица должна быть списком")
    #Проверка строк матрицы на null
    if not(all(row for row in matrix)):
        raise Exception("Строки матрицы не могут быть пустыми")
    #Проверка строк матрицы на то, что они - list
    if not(all(isinstance(row, list) for row in matrix)):
        raise Exception("Строки матрицы должны быть списками")
    #Проверка на то, что значения матрицы - int
    if not(all(isinstance(value, int) for row in matrix for value in row )):
        raise Exception("Элеметны матрицы должны быть типа int")
    #Проверка на квадратность
    if not(all(len(row) == len(matrix) for row in matrix)):
        raise Exception("Матрица должна быть квадратной")

def get_cropped_matrix(matrix: list[list[int]], i, j: int) -> list[list[int]]:
    """Возвращает квадратную матрицу без i-ой строки и j-ого столбца

    :param matrix: целочисленная квадратная матрица
    :i: индекс строки матрицы, который необходимо вырезать
    :j: индекс столбца матрицы, который необходимо вырезать
    :param matrix: целочисленная квадратная матрица
    :return: целочисленная квадратная матрица, 
    полученная из изначальной удалением i-ой строки и j-ого столбца
    """
    
    cropped_matrix = []
    for x in range(0, len(matrix)):
        if x == i: continue
        row = []
        for y in range (0, len(matrix)):
            if y == j: continue
            row.append(matrix[x][y])
        cropped_matrix.append(row)
    return cropped_matrix
    
def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :return: значение определителя
    """
    check_matrix(matrix)
    work_matrix = get_deep_copied_matrix(matrix)
    return calculate_determinant_rec(work_matrix)

def get_deep_copied_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Возвращает глубокую копию матрицы

    :param matrix: целочисленная квадратная матрица
    :return: глубокая копия целочисленной квадратной матрицы
    """
    
    copied_matrix = []
    for i in range(0, len(matrix)):
        row = []
        for j in range(0, len(matrix[i])):
            row.append(matrix[i][j])
        copied_matrix.append(row)
    return copied_matrix

def calculate_determinant_rec(matrix: list[list[int]]) -> int:
    """Возвращает детерминант матрицы

    :param matrix: целочисленная квадратная матрица
    :return: значение детерминанта 
    """
    if len(matrix) == 1:
        return matrix[0][0]
    else:
        det = 0
        for j in range(0, len(matrix)):
            complement = (-1) ** j * calculate_determinant_rec(get_cropped_matrix(matrix, 0, j))
            det += complement * matrix[0][j]
        return det
        
def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")

if __name__ == "__main__":
    main()
