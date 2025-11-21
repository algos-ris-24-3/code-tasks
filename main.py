def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    throw_exception(matrix)

    result = basic_calculate_determinant(matrix)
    return (result)


    
def basic_calculate_determinant(matrix: list[list[int]]) -> int:

    if len(matrix) == 1: 
        return matrix[0][0]
    
    det = 0 
    for index, value in enumerate(matrix[0]):
        det += value * (-1) ** index * basic_calculate_determinant(_get_minor(matrix, 0, index))
    return det

def throw_exception(matrix):
   if not matrix or not isinstance(matrix, list):
      raise Exception("error: matrix was not given")
   if len(matrix) != len(matrix[0]): 
       raise Exception("error: matrix is not square")

def _get_minor(matrix, row_index, col_index): 
    length_matrix = len(matrix)
    minor = []
    for i in range(length_matrix):
        if i == row_index:
            continue
        row = []
        for j in range(length_matrix):
            if j == col_index:
                continue
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
