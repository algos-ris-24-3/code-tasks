def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель целочисленной квадратной матрицы

    :param matrix: целочисленная квадратная матрица
    :raise Exception: если значение параметра не является целочисленной
    квадратной матрицей
    :return: значение определителя
    """
    def check_input_data(matrix):

        return basic_calculate_determinant(matrix)


    
def basic_calculate_determinant(matrix: list[list[int]]) -> int:

    if len(matrix) == 1: 
        return matrix[0][0]
    
    det = 0 
    for index, value in enumerate(matrix[0]):
        det += value * (-1) ** index * basic_calculate_determinant(_get_matrix_lower(matrix, 0, index))
    return det

def check_data(matrix):
    if not matrix or not isinstance(matrix, list):
        raise Exception("error: matrix was not given")
    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise Exception("error: matrix is not square")
    if n == 0: 
        raise Exception("error: matrix is empty")

def _get_matrix_lower(matrix, row_index, col_index): 
    length_matrix = len(matrix)
    matrix_lower = []
    for i in range(length_matrix):
        if i == row_index:
            continue
        row = []
        for j in range(length_matrix):
            if j == col_index:
                continue
            row.append(matrix[i][j])
        matrix_lower.append(row)
    return matrix_lower


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
